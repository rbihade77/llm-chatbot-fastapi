from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print("Loaded key prefix:", api_key[:6] if api_key else "None")

# Configure Gemini
genai.configure(api_key=api_key)

app = FastAPI()

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return {"message": "FastAPI with Google Gemini is running 🎉"}

@app.get("/test-gemini")
async def test_gemini():
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content("Say hello from FastAPI using Google Gemini 2.5")
        return {"reply": response.text}
    except Exception as e:
        return {"error": str(e)}

@app.get("/chat")
async def chat(message: str = Query(...)):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(message)
        return {"reply": response.text}
    except Exception as e:
        return {"error": str(e)}
