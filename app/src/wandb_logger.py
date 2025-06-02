import wandb
import os

def log_feedback(query, response, prompt_version, rating):
    wandb.init(project="GenA11yHelper", entity=os.getenv("bhstimpy-promptpilot"))
    wandb.log({
        "query": query,
        "response": response,
        "prompt_version": prompt_version,
        "user_rating": rating
    })
