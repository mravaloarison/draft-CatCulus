import os
import requests

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
AUTH_TOKEN = os.getenv("CLOUDFLARE_AUTH_TOKEN")

def generate_quiz():
    response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-2-7b-chat-fp16",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
        "messages": [
            {"role": "system", "content": "You are a friendly assistant"},
            {"role": "user", "content": """
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

            """}
        ]}
    )
    result = response.json()

    return result