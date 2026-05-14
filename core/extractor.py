import os
import cv2
import numpy as np
import pypdf as pdf
import easyocr as ocr

from pdf2image import convert_from_path


# load OCR once
ocr_reader = ocr.Reader(['en'], gpu=False)


def extract_text_from_pdf(pdf_path):

    reader = pdf.PdfReader(pdf_path)

    text = ""

    for i, page in enumerate(reader.pages):

        temp = page.extract_text()

        # normal text extraction
        if temp and temp.strip():

            text += temp + "\n"

        # OCR fallback
        else:

            convert_kwargs = {
                "pdf_path": pdf_path,
                "first_page": i + 1,
                "last_page": i + 1,
            }

            # windows poppler path
            if os.name == "nt":

                convert_kwargs["poppler_path"] = (
                    r"C:\other apps\poppler-26.02.0\Library\bin"
                )

            images = convert_from_path(**convert_kwargs)

            img = np.array(images[0])

            # resize for faster OCR
            img = cv2.resize(
                img,
                (img.shape[1] // 2, img.shape[0] // 2)
            )

            results = ocr_reader.readtext(
                img,
                detail=0
            )

            for txt in results:

                text += txt + "\n"

    return text