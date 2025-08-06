import os
import google.generativeai as genai

class GeminiService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_response(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response.text.strip()
