import streamlit as st  
from prompt_utils import get_response
from wandb_logger import log_feedback
from prompt_utils import get_current_prod_prompt
from dotenv import load_dotenv

load_dotenv()

# init
st.title("GenA11yHelper")
prompt_version = get_current_prod_prompt()

# handle input
query = st.text_input("Ask a question:")
if query:  
    response = get_response(query, prompt_version)  
    st.write(response)  
    
    # feedback
    rating = st.slider("Rate this response (1-5)", 1, 5, 3)
    if st.button("Submit Feedback"):
        log_feedback(query, response, prompt_version, rating)
        st.success("Feedback logged")
