import os
import shutil
import tempfile

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from resume_reader import extract_text_from_pdf, split_text_into_chunks
from vector_store import EndeeVectorStore
from qa_model import answer_question

app = FastAPI(title="AI Resume Analyzer")
templates = Jinja2Templates(directory="templates")

# Shared state
store = EndeeVectorStore()
resume_text: str = ""


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    global resume_text

    suffix = os.path.splitext(file.filename or "resume.pdf")[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        resume_text = extract_text_from_pdf(tmp_path)
    finally:
        os.unlink(tmp_path)

    if not resume_text:
        return {"status": "error", "message": "Could not extract text from the PDF."}

    chunks = split_text_into_chunks(resume_text)
    store.clear()
    store.add_chunks(chunks)

    return {
        "status": "ok",
        "message": f"Resume uploaded and indexed ({len(chunks)} sections).",
        "preview": resume_text[:500],
    }


@app.post("/ask")
async def ask_question(question: str = Form(...)):
    if not store.chunks and not resume_text:
        return {"answer": "Please upload a resume first."}

    relevant_chunks = store.search(question, top_k=5)
    answer = answer_question(
        question=question,
        context_chunks=relevant_chunks,
        full_text=resume_text,
    )
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
