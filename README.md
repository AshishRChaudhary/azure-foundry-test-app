# Azure OpenAI test project

## Setup

The virtual environment lives **outside** this folder, at
`C:\Users\cashi\.venvs\azure101`, so OneDrive doesn't sync thousands
of package files.

Recreate it from scratch:

```powershell
py -3.13 -m venv C:\Users\cashi\.venvs\azure101
C:\Users\cashi\.venvs\azure101\Scripts\python.exe -m pip install -r requirements.txt
```

## Secrets

Copy `.env.example` to `.env` and fill in your key:

```
AZURE_OPENAI_API_KEY=<your key>
AZURE_OPENAI_ENDPOINT=<your endpoint>
AZURE_OPENAI_DEPLOYMENTS=gpt-5.4-nano,gpt-5.6-sol
```

Keep a backup of the key somewhere outside this folder -- `.env` is the only
copy, and overwriting it loses both the key and your model list.

`.env` is gitignored and must never be committed. `config.py` loads it
and fails with a clear message if a value is missing.

## Summarizer app

```powershell
C:\Users\cashi\.venvs\azure101\Scripts\streamlit.exe run app.py
```

Opens at http://localhost:8501. Upload a PDF/DOCX/TXT or paste text, pick a
model in the sidebar, hit Summarize.

**Switching models.** The picker is driven by one line in `.env`:

```
AZURE_OPENAI_DEPLOYMENTS=gpt-5.4-nano,gpt-5.6-sol
```

The **first name is the default selection**. To add a model, append its
deployment name to the list and refresh the page -- the value is re-read on
every run, so no server restart is needed. Duplicates and stray whitespace
are ignored.

Names must match the deployment names in the Azure AI Foundry portal exactly;
a mismatch shows up as a 404, and the app says so explicitly. Note that the
endpoint advertises Azure's whole catalog (436 models) but this resource only
serves what's actually deployed on it.

## Running the API smoke test

VS Code picks up the venv automatically via `.vscode/settings.json`.
Reload the window if the interpreter doesn't switch.

From a terminal:

```powershell
C:\Users\cashi\.venvs\azure101\Scripts\python.exe test_azure_api.py
```

## Dependencies

- `requirements.txt` — direct dependencies, pinned.
- `requirements.lock.txt` — full transitive set, for exact reproduction.
