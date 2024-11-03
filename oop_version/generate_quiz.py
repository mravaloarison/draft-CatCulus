import google.generativeai as genai
import os, json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt_to_json_model = genai.GenerativeModel("gemini-1.5-flash", 
    generation_config = {"response_mime_type": "application/json"})
regular_model = genai.GenerativeModel("gemini-1.5-flash")

def generate_quiz():
    # prompt = os.getenv("YOUR_PROMPT")
    prompt = """
    Generate 5 math-based quizzes that meet the following criteria:
        - Each question should involve two unknown numbers, x and y, and use all addition, subtraction, multiplication, square, cube, or other mathematical operations.
        - Don't Always use the same operation for each question.
        - Ensure x and y are always less than or equal to 5 in value.
        - The challenge should be for the user to guess x and y based on the given equation.
        - The instruction should not reveal that the numbers are less than 5.
        - Examples:
            * 'instructions': 'Find the two numbers, x and y, that satisfy the equation: x + y = 10.', 'combinations': [[5, 5]]
            -> Explanation: The only combination of x and y that satisfies the equation x + y = 10 is 5 + 5 = 10.

            * 'instructions': 'What are the two numbers, x and y, that satisfy the equation: x - y = -1?', 'combinations': [[0,1],[1,2], [2, 3], [3, 4], [4, 5]]
            -> Explanation: The combinations of x and y that satisfy the equation x - y = -1 are 0 - 1 = -1, 1 - 2 = -1, 2 - 3 = -1, 3 - 4 = -1, and 4 - 5 = -1.

            * 'Find the two numbers, x and y, that fulfill the equation: x / y = 2.', 'combinations': [[4, 2]]
            -> Explanation: The only combination of x and y that satisfies the equation x / y = 2 is 4 / 2 = 2.
            ....
        - Return the output in a JSON object format with the following structure:

        sign: str
        answer: int 
        instructions: str 
        combinations: List[Tuple[int, int]] 
        Returns: [answer, instructions, combinations]
    """

    response = prompt_to_json_model.generate_content(prompt)
    array_of_keywords = json.loads(response.text)

    return array_of_keywords

print(generate_quiz())