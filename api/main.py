from fastapi import FastAPI, UploadFile, File
import shutil

from core.pipeline import summarize_pipeline


app = FastAPI()


@app.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):

    temp_path = "temp.pdf"

    # save uploaded file
    with open(temp_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    # run Revizen pipeline
    notes = summarize_pipeline(temp_path)

    return {
        "filename": file.filename,
        "notes": notes
    }

