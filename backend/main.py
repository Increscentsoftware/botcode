import os
from dotenv import load_dotenv

# Load environment variables from .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# Explicitly set the environment variable
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AzureOpenAI, OpenAIError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Get values
API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT")

# Validate
if not API_KEY or not AZURE_ENDPOINT or not DEPLOYMENT_NAME:
    raise RuntimeError("❌ Missing one or more required environment variables.")

# Init OpenAI client
client = AzureOpenAI(
    api_key=API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version="2025-01-01-preview"
)

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class PromptRequest(BaseModel):
    prompt: str
    model: str

# Endpoint for AI
@app.post("/api/run")
async def run_ai(req: PromptRequest):
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": req.prompt}
            ],
            max_tokens=800,
            temperature=1.0
        )
        return {"output": response.choices[0].message.content}
    except OpenAIError as e:
        return {"output": f"❌ OpenAI error: {str(e)}"}
    except Exception as e:
        return {"output": f"❌ General error: {str(e)}"}

# ✅ Serve frontend static site (Next.js export)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")
