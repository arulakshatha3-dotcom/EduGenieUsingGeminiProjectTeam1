import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=API_KEY)

PRIMARY_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

FALLBACK_MODELS = [
    PRIMARY_MODEL,
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]


def generate_text(
    prompt: str,
    temperature: float = 0.7,
    max_output_tokens: int = 2048
) -> str:

    last_error = None

    for model in FALLBACK_MODELS:

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_output_tokens,
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(
                            disable=True
                        )
                    )
                )

                return response.text or ""

            except ServerError as error:

                last_error = error

                if "503" in str(error):
                    time.sleep(2 ** attempt)
                    continue

                raise

    raise RuntimeError(
        "Gemini models are temporarily unavailable. "
        f"Last error: {last_error}"
    )