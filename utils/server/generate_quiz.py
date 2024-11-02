import google.generativeai as genai
import os, json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt_to_json_model = genai.GenerativeModel("gemini-1.5-flash", 
    generation_config = {"response_mime_type": "application/json"})
regular_model = genai.GenerativeModel("gemini-1.5-flash")

def generate_quiz():
    prompt = os.getenv("YOUR_PROMPT")

    response = prompt_to_json_model.generate_content(prompt)
    array_of_keywords = json.loads(response.text)

    return array_of_keywords