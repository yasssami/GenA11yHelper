# GenA11yHelper


Project Name: **GenA11yHelper**

Group Name: **Prompt Pilot**

Main Participant Name: **Yassine Sami**

Team Participant Names: 

Mihir Soni,
Dondre Samuels,
Vaishali Jaiswal

--------------------------------------------

AWS Code:

Yassine Sami: PC36VH5465GGNF1 

Mihir Soni: PC245ZI84HVWW41

Dondre Samuels: PC3N2GR7I3A6020 

Vaishali Jaiswal: PC1K0K43P3W1753 


### For Credit details please Contact administrator on Slack

**https://app.slack.com/huddle/T01BN24U54L/C08SF5BUGN4**

--------------------------------------------

GenA11yHelper
Smarter Prompt Testing for GenAI – Deployed with Terraform and AWS
## Project Overview
“GenA11yHelper” is a lightweight DevOps-powered GenAI tool that helps teams experiment with different large language model (LLM) prompts. Users can test prompts, rate the AI’s responses, and automatically promote the best-performing ones. This workflow makes it easier to improve prompt quality over time by using real user feedback, helping teams build smarter, more effective GenAI applications.
## How It Works
	Frontend Interface: A Streamlit + LangChain app inside a Docker container allows users to input data and test prompts.
	LLM Querying: Prompts are processed via the OpenAI API to generate responses.
	User Rating: Each response is rated (e.g., thumbs up/down), simulating real user feedback.
	Prompt Versioning: Prompt templates are versioned and stored in an AWS S3 bucket.
	Feedback Logging: Ratings are logged (planned via Weights & Biases).
	DevOps Automation: GitHub Actions CI/CD is used to update the best-performing prompts in a GitHub repo (`prompt-templates/`).
## Technologies Used
	Terraform – Infrastructure as Code (IaC)
	AWS EC2 – Hosts the containerized app
	AWS S3 – Stores versioned prompt templates
	Streamlit + LangChain – Web app frontend
	Docker – Container environment
	OpenAI API – LLM querying
	GitHub Actions – Prompt promotion via CI/CD
	Weights & Biases (planned) – Feedback visualization and logging

## AWS Infrastructure (via Terraform)
	Sets up a secure S3 bucket to store prompt versions
	Launches a small Ubuntu server (EC2) using the free tier
	Installs Docker on the server to run the app
	Opens ports for the app (8501) and SSH access (22)
	Creates SSH keys for secure login
	Displays the server's public IP and login details

## Repository Structure
/terraform/    → Infrastructure code  
flowchart.png    → System architecture  
prompt-templates/   → (Planned) Prompt storage  
README.md    → This file  

## Notes
Hackathon: DevOps for GenAI 2025  
Track 5: Prompt Testing & Experimentation  
AWS cloud environment provided by the organizers  
Project built within an 8-hour hackathon window  


