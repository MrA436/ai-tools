import os
import cv2
import numpy as np
import streamlit as st
import pypdf as pdf
import easyocr as ocr
from groq import Groq
from dotenv import load_dotenv
from pdf2image import convert_from_path

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

model = "llama-3.1-8b-instant"

@st.cache_resource
def load_ocr():
    return ocr.Reader(['en'], gpu=False)

ocr_reader = load_ocr()

def extract_text_from_pdf(pdf_path):
    reader = pdf.PdfReader(pdf_path)
    text = ''

    for i, page in enumerate(reader.pages):

        temp = page.extract_text()

        if temp and temp.strip():

            text += temp + '\n'

        else:
            convert_kwargs = {
                "pdf_path": pdf_path,
                "first_page": i + 1,
                "last_page": i + 1,
            }

            if os.name == "nt":
                convert_kwargs["poppler_path"] = r"C:\other apps\poppler-26.02.0\Library\bin"

            images = convert_from_path(**convert_kwargs)

            img = np.array(images[0])

            img = cv2.resize(
                img,
                (img.shape[1] // 2, img.shape[0] // 2)
            )

            results = ocr_reader.readtext(img, detail=0)

            for txt in results:
                text += txt + '\n'
    return text


def generate_notes(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())

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
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error generating notes: {str(e)}"

def delete_temp_file():
    if os.path.exists("temp.pdf"):
        os.remove("temp.pdf")
    