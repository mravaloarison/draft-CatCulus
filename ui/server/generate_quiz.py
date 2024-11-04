import google.generativeai as genai
import os, json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


prompt_to_json_model = genai.GenerativeModel("gemini-1.5-flash", 
    generation_config = {"response_mime_type": "application/json"})
regular_model = genai.GenerativeModel("gemini-1.5-flash")

def generate_quiz():
    # prompt = os.getenv("YOUR_PROMPT")
    prompt = "Create 10 quizzes with math like ___ + ___ = 14 \n- but make them guess 2 numbers, both less than 10 \n- you can eve use something square somethign is equal your numbers, \n- then return to me a JSON object with the questions and answers as below \nx: int \ny: int \nanswer: int \ninstructions: str \ncombinations: List[Tuple[int, int]] \nReturns: [x, y, answer, instructions, combinations]"

    response = prompt_to_json_model.generate_content(prompt)
    array_of_keywords = json.loads(response.text)

    return array_of_keywords

generate_quiz()