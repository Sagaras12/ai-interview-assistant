from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_feedback(question, answer):

    prompt = f"""
Question: {question}

Answer: {answer}

Give interview feedback with:
1. Score out of 10
2. Strength
3. Weakness
4. Improvement
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"⚠️ API Error: {str(e)}"