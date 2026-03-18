from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-large"

_tokenizer = None
_model = None


def _load_model():
    global _tokenizer, _model
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        _model.eval()
    return _tokenizer, _model


def _generate(prompt: str, max_tokens: int = 300) -> str:
    """Run a prompt through Flan-T5 and return generated text."""
    tokenizer, model = _load_model()
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=3,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


def answer_question(
    question: str,
    context_chunks: list[str],
    full_text: str = "",
) -> str:
    """Answer a question about the resume using retrieved chunks + full text.

    Strategy:
    1. Try with the most relevant chunks first (focused context).
    2. If the answer is weak, retry with the full resume text.
    """
    if not context_chunks and not full_text:
        return "No resume data available. Please upload a resume first."

    # --- Attempt 1: answer from relevant chunks ---
    chunk_context = "\n\n".join(context_chunks)
    prompt = _build_prompt(question, chunk_context)
    answer = _generate(prompt)

    # If the answer is too short or looks incomplete, try with full text
    if full_text and (not answer or len(answer.split()) < 3):
        # Truncate full text to fit in model window
        words = full_text.split()[:600]
        full_context = " ".join(words)
        prompt = _build_prompt(question, full_context)
        answer = _generate(prompt)

    if not answer:
        return "I couldn't find a clear answer in the resume for that question."
    return answer


def _build_prompt(question: str, context: str) -> str:
    """Build a detailed instruction prompt for Flan-T5."""
    return (
        f"You are analyzing a candidate's resume. "
        f"Answer the question accurately and in detail based only on the resume content below.\n\n"
        f"Resume content:\n{context}\n\n"
        f"Question: {question}\n"
        f"Provide a complete and detailed answer:"
    )
