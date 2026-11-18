import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"


def ask_gemini(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return response.text

        except errors.ServerError as error:
            if attempt == max_retries - 1:
                raise RuntimeError(
                    "Gemini is temporarily unavailable. "
                    "Please try again later."
                ) from error

            time.sleep(2 ** (attempt + 1))

