import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.1-8b-instant"


def generate_notes(text):

    # cleanup
    text = text.replace("\n", " ")
    text = " ".join(text.split())

    # temporary limit
    text = text[:8000]

    prompt = f"""
    Create:

    1. Clean Summary
    2. Important Exam Questions with Answers
    3. Revision Notes
    4. Important Keywords

    Rules:
    - Keep output concise
    - Use markdown formatting
    - Use bullet points
    - Focus only on important exam concepts
    - Do not add information outside the notes

    Study Material:
    {text}
    """

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error generating notes: {str(e)}"