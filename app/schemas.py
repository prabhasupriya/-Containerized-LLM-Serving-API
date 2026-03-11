from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: Optional[int] = 50

class GenerateResponse(BaseModel):
    generated_text: str