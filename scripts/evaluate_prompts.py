import wandb  
import boto3  
import pandas as pd  

# init  
api = wandb.Api()  
s3 = boto3.client("s3")  

def fetch_prompt_metrics():  
    """Collect metrics for w&b prompts"""  
    runs = api.runs("gena11yhelper/project")  
    data = []  
    for run in runs:  
        if run.config.get("prompt_version"):  
            data.append({  
                "prompt_version": run.config["prompt_version"],  
                "completion_rate": run.summary.get("completion_rate", 0),  
                "avg_rating": run.summary.get("user_rating", 0),  
                "run_id": run.id  
            })  
    return pd.DataFrame(data)  

def calc_best_prompt(df):  
    """select prompt w/ highest weighted score"""  
    df["score"] = (  
        df["completion_rate"] * 0.5 +  
        df["avg_rating"] * 0.5  
    )  
    return df.loc[df["score"].idxmax()]["prompt_version"]  

if __name__ == "__main__":  
    # analyze metrics  
    df = fetch_prompt_metrics()  
    best_prompt = calc_best_prompt(df)  

    # save winning prompt  
    with open("winning_prompt.txt", "w") as f:  
        f.write(best_prompt)  

    print(f"Best prompt: {best_prompt}")  