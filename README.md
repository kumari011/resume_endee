# AI Resume Analyzer

Upload any PDF resume and ask questions about it — skills, education, experience, name, contact info, and more. Fully local, no API keys needed.

**Powered by:** Endee vector database abstraction | Flan-T5-Large | Sentence-Transformers

---

## Quick Start (1 command)

### Windows
```
Double-click run.bat
```
Or from PowerShell:
```
.\run.bat
```

### Linux / macOS
```
chmod +x run.sh && ./run.sh
```

That's it! The browser will open automatically at **http://127.0.0.1:8000**

---

## What it does

1. **Upload** a PDF resume
2. **Ask** any question about the candidate
3. **Get answers** powered by local AI (no internet needed after first run)

Example questions:
- What are the candidate's skills?
- What is the candidate's name?
- Education details?
- Work experience?
- Contact information?
- Projects done?

---

## Requirements

- **Python 3.10+** (https://www.python.org/downloads/)
- ~4 GB disk space (for AI models, downloaded once on first run)
- ~4 GB RAM

All Python packages are installed automatically by the run script.

---

## Project Structure

```
app.py              → FastAPI server
resume_reader.py    → PDF text extraction + section-aware chunking
vector_store.py     → Endee vector store (embeddings + search)
qa_model.py         → Flan-T5-Large question answering
templates/index.html→ Web UI
requirements.txt    → Python dependencies
run.bat             → Windows one-click launcher
run.sh              → Linux/macOS one-click launcher
```

---

## Tech Stack

| Component    | Technology                          |
|-------------|-------------------------------------|
| Backend     | FastAPI + Uvicorn                   |
| PDF Parser  | pdfplumber (layout-aware)           |
| Embeddings  | sentence-transformers (MiniLM-L6)   |
| Vector DB   | EndeeVectorStore (custom)           |
| QA Model    | google/flan-t5-large (local)        |
| Frontend    | HTML + CSS + vanilla JS             |
