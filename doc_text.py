"""Extract plain text from an uploaded document."""

import io


def extract(uploaded_file) -> str:
    """Return the text content of a Streamlit UploadedFile."""
    name = (uploaded_file.name or "").lower()
    raw = uploaded_file.getvalue()

    if name.endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(raw))
        pages = [(p.extract_text() or "") for p in reader.pages]
        return "\n\n".join(pages).strip()

    if name.endswith(".docx"):
        import docx

        doc = docx.Document(io.BytesIO(raw))
        return "\n".join(p.text for p in doc.paragraphs).strip()

    # .txt, .md, .csv and anything else we treat as plain text
    for encoding in ("utf-8", "utf-16", "latin-1"):
        try:
            return raw.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace").strip()
