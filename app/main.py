import os
import anyio
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Optional
from transformers import pipeline
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# 1. Validation Schemas
class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: Optional[int] = 50

class GenerateResponse(BaseModel):
    generated_text: str

# 2. Lazy-Loading Model Singleton
class LLMModel:
    _instance = None
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            print("--- Loading model into memory (Lazy Load) ---")
            model_name = os.getenv("MODEL_NAME", "gpt2")
            cls._instance = pipeline("text-generation", model=model_name)
        return cls._instance

def perform_inference(prompt: str, max_tokens: int):
    model = LLMModel.get_instance()
    result = model(prompt, max_new_tokens=max_tokens, num_return_sequences=1)
    return result[0]['generated_text']

# 3. API Setup & Security
app = FastAPI(title="Production LLM API", version="1.0.0")
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def validate_api_key(api_key: str = Depends(api_key_header)):
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key. Use 'X-API-KEY' header."
        )
    return api_key

# 4. Endpoints
@app.get("/health")
async def health():
    return {"status": "200 OK", "message": "Service is running"}

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest, _ = Depends(validate_api_key)):
    # Concurrency: Use thread pool for CPU-bound inference
    output = await anyio.to_thread.run_sync(
        perform_inference, request.prompt, request.max_new_tokens
    )
    return {"generated_text": output}