import os
import time

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Model to use
MODEL_NAME = "gemini-3.5-flash"
# If you want, you can later change it to:
# MODEL_NAME = "gemini-3.5-flash"


def ask_ai(question):
    """
    Sends a question to Gemini and returns the response.
    Retries automatically if the server is temporarily busy.
    """

    prompt = f"""
You are an AI expert in:

• Climate Change
• Sustainability
• Renewable Energy
• Carbon Emissions
• Environmental Science
• Air Quality

Give professional, accurate and concise answers.

Question:
{question}
"""

    retries = 3

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error = str(e)

            # Retry only if server is busy
            if "503" in error or "UNAVAILABLE" in error:

                if attempt < retries - 1:
                    time.sleep(3)
                    continue

                return (
                    "⚠️ Gemini servers are currently experiencing high demand.\n\n"
                    "Please try again after a few moments."
                )

            # Authentication error
            elif "401" in error:

                return (
                    "❌ Invalid API Key.\n\n"
                    "Please check your GEMINI_API_KEY in the .env file."
                )

            # Model error
            elif "404" in error:

                return (
                    "❌ Selected Gemini model is unavailable.\n\n"
                    "Please change MODEL_NAME in utils/gemini.py."
                )

            # Any other error
            else:

                return f"⚠️ Error:\n\n{error}"