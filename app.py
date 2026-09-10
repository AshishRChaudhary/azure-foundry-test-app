"""Basic document summarizer for testing Azure AI Foundry deployments."""

import time
from urllib.parse import urlparse

import streamlit as st

import config
import doc_text

MAX_CHARS = 120_000  # keep a single request inside a sane context budget

LENGTHS = {
    "Short (3 bullets)": "Summarize in exactly 3 short bullet points.",
    "Medium (1 paragraph)": "Summarize in one tight paragraph.",
    "Detailed (sectioned)": (
        "Summarize with headings: Overview, Key Points, Details, Takeaways."
    ),
}

st.set_page_config(page_title="Doc Summarizer", page_icon="📄", layout="wide")

# --------------------------------------------------------------------------
# Sidebar: model switching + summary options
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("Model")
    st.caption(f"Endpoint: `{urlparse(config.AZURE_OPENAI_ENDPOINT).hostname}`")

    # Re-read on every run, so editing AZURE_OPENAI_DEPLOYMENTS in .env
    # shows up on a page refresh.
    try:
        choices = config.deployments()
    except RuntimeError as exc:
        st.error(str(exc))
        st.stop()

    model = st.radio(
        f"Deployment ({len(choices)})",
        choices,
        index=0,  # first name in AZURE_OPENAI_DEPLOYMENTS is the default
        help="Edit AZURE_OPENAI_DEPLOYMENTS in .env to add or reorder these.",
    )

    st.divider()
    st.header("Summary")
    length = st.radio("Length", list(LENGTHS), index=1)
    focus = st.text_input("Focus (optional)", placeholder="e.g. risks, costs")
    max_tokens = st.slider("Max output tokens", 500, 8000, 3000, step=500)

# --------------------------------------------------------------------------
# Main: input
# --------------------------------------------------------------------------
st.title("📄 Document Summarizer")
st.caption(f"Active model: **{model}**")

upload_tab, paste_tab = st.tabs(["Upload a file", "Paste text"])
with upload_tab:
    upload = st.file_uploader(
        "PDF, DOCX, TXT, MD or CSV", type=["pdf", "docx", "txt", "md", "csv"]
    )
with paste_tab:
    pasted = st.text_area("Text", height=220)

text = ""
if upload is not None:
    try:
        text = doc_text.extract(upload)
    except Exception as exc:
        st.error(f"Couldn't read that file: {exc}")
elif pasted.strip():
    text = pasted.strip()

if text:
    st.caption(f"{len(text):,} characters · ~{len(text) // 4:,} tokens")
    if len(text) > MAX_CHARS:
        st.warning(
            f"Truncating to the first {MAX_CHARS:,} characters for this test app."
        )
        text = text[:MAX_CHARS]
    with st.expander("Extracted text"):
        st.text(text[:3000] + ("…" if len(text) > 3000 else ""))

# --------------------------------------------------------------------------
# Main: summarize
# --------------------------------------------------------------------------
if st.button("Summarize", type="primary", disabled=not text):
    prompt = LENGTHS[length]
    if focus.strip():
        prompt += f" Pay particular attention to: {focus.strip()}."

    st.subheader("Summary")
    started = time.time()
    try:
        stream = config.client().chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You summarize documents faithfully."},
                {"role": "user", "content": f"{prompt}\n\n---\n{text}"},
            ],
            max_completion_tokens=max_tokens,
            stream=True,
        )
        chunks = (
            c.choices[0].delta.content or "" for c in stream if c.choices
        )
        answer = st.write_stream(chunks)

        elapsed = time.time() - started
        if answer:
            st.caption(f"{model} · {elapsed:.1f}s")
        else:
            st.warning(
                "The model returned nothing. Reasoning models spend the token "
                "budget on thinking first -- raise 'Max output tokens'."
            )
    except Exception as exc:
        detail = str(exc)
        if "404" in detail or "DeploymentNotFound" in detail:
            st.error(
                f"`{model}` isn't deployed on this resource. Check the name in "
                "AZURE_OPENAI_DEPLOYMENTS against the Azure portal -- it must "
                "match the deployment name exactly."
            )
        else:
            st.error(f"{type(exc).__name__}: {detail}")
