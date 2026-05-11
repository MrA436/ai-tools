import pypdf as pdf
from groq import Groq
from dotenv import load_dotenv
import os
import easyocr as ocr
import pdf2image

load_dotenv()

client = Groq(
    api_key= os.getenv("GROQ_API_KEY")
)

model="llama-3.1-8b-instant"
ocr_reader = ocr.Reader(['en'])

def extract_text_from_pdf(pdf_path):
    reader = pdf.PdfReader(pdf_path)
    images  = None
    text = ''
    for i, page in enumerate(reader.pages):
        temp = page.extract_text()
        if temp:
            text += temp + '\n'
        else:
            if images is None:
                images  = pdf2image.convert_from_path(pdf_path)
            img = images[i]
            results = ocr_reader.readtext(img, detail=0)
            for txt in results:
                text += txt + '\n'
    return text

def generate_notes(text):
    prompt = f"""
        You are an intelligent exam-focused study assistant.

        Analyze the provided study material and generate highly useful student revision content.

        Instructions:

        * Keep explanations concise and easy to understand.
        * Focus only on the most important concepts.
        * Do NOT add information not present in the notes.
        * Use clean markdown formatting.
        * Avoid long paragraphs.
        * Use bullet points wherever possible.

        Generate the output in the following structure:

        # Clean Summary

        * Provide a concise but complete summary of the topic.
        * Explain important ideas in simple language.
        * Focus on concepts most likely to appear in exams.

        # Important Exam Questions

        Generate:

        * Short answer questions with concise answers
        * 5-mark questions with structured answers
        * Long answer/theory questions with detailed answers
        * Viva questions with direct one-line answers if applicable

        Formatting Rules:

        * Write each question first
        * Then provide its answer directly below it
        * Keep answers concise but exam-ready
        * Use bullet points wherever possible`

        Study Material:
        {text}
    """
    response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=model)
    notes = response.choices[0].message.content
    return notes

