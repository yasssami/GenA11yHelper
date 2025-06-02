import os
import boto3
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain.chains import LLMChain
import time
import traceback
from datetime import datetime
import wandb
from collections import deque

feedback_queue = deque(maxlen=100)


#TODO see if we don't wanna change this
DEFAULT_PROMPT = """You are a helpful AI assistant with extensive expertise. Provide clear, concise answers to user questions with precision as a core tenet.

Question: {query}
Answer:"""

llm = OpenAI(
    temperature=0.35,
    model_name="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def load_prompt_template(prompt_version):
    s3 = boto3.client("s3")
    try:
        response = s3.get_object(
            Bucket="gena11yhelper-prompts-3aa050f0",
            Key=f"prompts/{prompt_version}.txt"
        )
        return response["Body"].read().decode("utf-8")
    except Exception as e:
        print(f"Prompt load error: {e}")
        return DEFAULT_PROMPT
    

def get_current_prod_prompt():  
    s3 = boto3.client("s3")  
    try:  
        response = s3.get_object(
            Bucket="gena11yhelper-prompts-3aa050f0",  
            Key="production.txt"  
        )  
        return response["Body"].read().decode("utf-8").strip()  
    except:  
        return "v2.txt"  # fallback
    
def get_response(query: str, prompt_version: str) -> str:
    """Get LLM response using versioned prompt template with full tracking"""
    prompt_text = load_prompt_template(prompt_version)
    
    # langchain template init
    prompt = PromptTemplate(
        input_variables=["query"],
        template=prompt_text
    )
    
    # init w&b
    run = wandb.init(
        project="GenA11yHelper",
        config={
            "prompt_version": prompt_version,
            "model": "gpt-4o-mini",
            "temperature": 0.35,
            "chain_type": "LLMChain"
        },
        reinit=True,
        tags=["inference"]
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    start_time = time.time()
    
    try:
        response = chain.run(query=query)
        latency = time.time() - start_time
        
        # log to w&b
        run.log({
            "query": query,
            "response": response,
            "prompt_text": prompt_text,
            "prompt_version": prompt_version,
            "latency_seconds": latency,
            "response_length": len(response)
        })
        
        # push to feedback queue
        feedback_queue.append({
            "query": query,
            "response": response,
            "prompt_version": prompt_version,
            "timestamp": datetime.utcnow().isoformat(),
            "run_id": run.id
        })
        
    except Exception as e:
        # errlog
        run.log({
            "error": str(e),
            "stack_trace": traceback.format_exc()
        })
        response = f"Error generating response: {str(e)}"
    finally:
        run.finish()
    
    return response
