import re

import pdfplumber


# Common resume section headings (case-insensitive matching)
_SECTION_PATTERNS = [
    r"objective",
    r"summary",
    r"profile",
    r"experience",
    r"work\s*experience",
    r"professional\s*experience",
    r"employment",
    r"education",
    r"academic",
    r"skills",
    r"technical\s*skills",
    r"core\s*competencies",
    r"certifications?",
    r"projects?",
    r"achievements?",
    r"awards?",
    r"publications?",
    r"languages?",
    r"interests?",
    r"hobbies",
    r"references?",
    r"contact",
    r"personal\s*(?:details|information|info)",
    r"declaration",
    r"strengths",
]
_SECTION_RE = re.compile(
    r"^[\s]*(?:" + "|".join(_SECTION_PATTERNS) + r")[\s:]*$",
    re.IGNORECASE | re.MULTILINE,
)


def _clean_spaced_text(text: str) -> str:
    """Collapse PDF artifacts like 'T E C H N I C A L' → 'TECHNICAL'."""
    def collapse(m: re.Match) -> str:
        return m.group(0).replace(" ", "")
    return re.sub(r"\b(?:[A-Za-z] ){2,}[A-Za-z]\b", collapse, text)


def _normalize(text: str) -> str:
    """Clean up whitespace while preserving meaningful line breaks."""
    text = re.sub(r"[ \t]+", " ", text)           # collapse horizontal space
    text = re.sub(r" *\n *", "\n", text)           # trim around newlines
    text = re.sub(r"\n{3,}", "\n\n", text)         # max 2 consecutive newlines
    return text.strip()


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF using pdfplumber (handles complex layouts)."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(
                layout=True, x_density=7.25, y_density=13
            )
            if page_text:
                text += page_text + "\n"
    text = _clean_spaced_text(text)
    text = _normalize(text)
    return text


def split_text_into_sections(text: str) -> list[str]:
    """Split resume text by detected section headings.

    Returns a list of section strings, each prefixed with its heading.
    If no sections are detected, falls back to fixed-size chunks.
    """
    matches = list(_SECTION_RE.finditer(text))

    if len(matches) < 2:
        # Fallback: fixed-size overlapping chunks
        return _fixed_chunks(text, chunk_size=150, overlap=30)

    sections: list[str] = []

    # Text before the first section heading (usually name + contact info)
    header = text[: matches[0].start()].strip()
    if header:
        sections.append(header)

    # Each section: heading → next heading
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[m.start() : end].strip()
        if section:
            sections.append(section)

    # If any section is very long, split it further
    result: list[str] = []
    for sec in sections:
        if len(sec.split()) > 250:
            result.extend(_fixed_chunks(sec, chunk_size=150, overlap=30))
        else:
            result.append(sec)

    return result


def _fixed_chunks(text: str, chunk_size: int = 150, overlap: int = 30) -> list[str]:
    """Split text into overlapping word-level chunks."""
    words = text.split()
    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


# Keep backward-compat alias
split_text_into_chunks = split_text_into_sections
