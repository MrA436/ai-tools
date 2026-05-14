from core.extractor import extract_text_from_pdf
from core.ai import generate_notes


def summarize_pipeline(pdf_path):

    #extracting text from pdf
    text = extract_text_from_pdf(pdf_path)

    #generate notes
    notes = generate_notes(text)

    return notes
