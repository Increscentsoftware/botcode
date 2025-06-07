from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AzureOpenAI
import os

# FastAPI app
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your frontend's origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class PromptRequest(BaseModel):
    prompt: str
    model: str  # "azure-gpt4" etc

# Azure OpenAI config
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://pramo-mbmd1udj-eastus2.cognitiveservices.azure.com/openai/deployments/Chatbot/chat/completions?api-version=2025-01-01-preview",
    api_key="19TU6mL7WuJSuxuKUGjqfX0F3KQtxg96J0jpHLhhT2M1KFcwM1nRJQQJ99BFACHYHv6XJ3w3AAAAACOG9hwp",
)

DEPLOYMENT_NAME = "Chatbot"  # This is what you named the deployment in Azure

@app.post("/api/run")
async def run_ai(req: PromptRequest):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": req.prompt}
            ],
            max_tokens=800,
            temperature=1.0,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            model=DEPLOYMENT_NAME
        )
        return {"output": response.choices[0].message.content}
    except Exception as e:
        print("Error:", str(e))
        return {"output": "Error: " + str(e)}
