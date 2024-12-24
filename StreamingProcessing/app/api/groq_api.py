import json
import os
from groq import Groq

from dotenv import load_dotenv

load_dotenv(verbose=True)
def post_groq_api(article_content: dict) -> dict:
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content":  (
                    f"{json.dumps(article_content)}\n\n"
                    "This is an article. I want to analyze a few things:\n"
                    "1. In what country did it happen?\n"
                    "2. Classify the article into one of the following categories: general news, historical terror attack, or nowadays terror attack.\n\n"
                    "After analyzing, provide a JSON with the following structure:\n"
                    "{\n"
                    "    \"category\": \"str\",\n"
                    "    \"country\": \"str\",\n"
                    "    \"city\": \"str\",\n"
                    "    \"continent\": \"str\",\n"
                    "    \"longitude\": \"int\",\n"
                    "    \"latitude\": \"int\",\n"
                    "}\n\n"
                    "If you cant find the city return the country longitude latitude instead"
                    "Respond with the JSON only, without any extra text."
                ),
            }
        ],
        model="llama3-8b-8192",
    )
    return json.loads(chat_completion.choices[0].message.content)