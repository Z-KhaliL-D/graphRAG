import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEN_API_KEY"))

def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(f"You are an AI research assistant. {prompt}")
    return response.text

def get_embedding(text):
    """
    Correct way to get embeddings with google-generativeai
    """
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return result['embedding']