import pypdf as pdf
from groq import Groq
from dotenv import load_dotenv
import os
import easyocr as ocr

load_dotenv()

client = Groq(
    api_key= os.getenv("GROQ_API_KEY")
)

model="llama-3.1-8b-instant"


reader = pdf.PdfReader('Sir_Deep_Analysis.pdf')

a = ''

for page in reader.pages:
    temp = page.extract_text()
    if temp:
        a += temp

prompt = f"""
Convert these notes into:

1. Clean summary
2. Important exam questions
3. Revision notes

Content:
{a}
"""
response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=model)
f = response.choices[0].message.content
op = open("output.txt", "w")
op.write(f)
op.close()