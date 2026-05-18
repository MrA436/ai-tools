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
    You are a calm, focused exam coach helping a student revise smart in the last hour before their exam.

    The student is stressed, short on time, and only wants the highest-yield information that helps them score marks quickly.

    Your job is NOT to rewrite the textbook.

    Your job is to:
    - simplify
    - prioritize
    - compress
    - highlight likely exam material
    - reduce panic
    - improve recall speed

    Study Material:
    {text}

    Return ONLY a valid JSON object.
    Do NOT return markdown.
    Do NOT return explanations.
    Do NOT wrap output in code fences.

    Use this EXACT JSON structure:

    {{
        "high_priority_revision": [
            "High-yield revision point here",
            "Important concept, formula, syntax, or exam-focused explanation here"
        ],

        "exam_questions": [
            {{
                "question": "Question text here?",
                "answer": "Short, direct answer that gets marks."
            }}
        ],

        "keywords": [
            {{
                "term": "Term",
                "definition": "One-line definition"
            }}
        ]
    }}

    CONTENT RULES (follow strictly):

    - high_priority_revision:
        - Include 6-10 highest-yield revision points only
        - Include concepts, formulas, syntax, definitions, edge cases, and commonly tested facts
        - Include things students commonly forget in exams
        - Keep every point concise, practical, and revision-focused
        - Each point should help the student score marks quickly
        - Avoid long explanations
        - Avoid generic textbook wording

    - exam_questions:
        - Include 4-6 most likely exam questions
        - Answers must be concise and mark-oriented
        - Focus on what a student should actually write in exams
        - Avoid overly theoretical answers

    - keywords:
        - Include only important technical terms
        - Definitions must be one line
        - Keep definitions easy to memorize quickly

    GLOBAL RULES:
    - No filler
    - No padding
    - No motivational talk
    - No unnecessary detail
    - No low-value theory
    - Prioritize recall speed and exam usefulness
    - Skip unclear information instead of inventing
    - Sound sharp, practical, and human
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