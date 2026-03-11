from transformers import pipeline
import torch

class LLMModel:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            print("Loading model for the first time...")
            # Using GPT-2 for a small, fast-loading image (under 1.5GB)
            cls._instance = pipeline("text-generation", model="gpt2")
        return cls._instance

def generate_text(prompt: str, max_tokens: int):
    model = LLMModel.get_instance()
    result = model(prompt, max_new_tokens=max_tokens, num_return_sequences=1)
    return result[0]['generated_text']