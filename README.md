# Azure Foundry Test App

A basic Streamlit document summarizer for exercising Azure AI Foundry
deployments. Upload a PDF/DOCX/TXT/MD/CSV or paste text, pick a model, and
get a streamed summary.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

`requirements.lock.txt` holds the full transitive set if you need to
reproduce the exact environment.

## Configuration

Copy `.env.example` to `.env` and fill it in:

```
AZURE_OPENAI_API_KEY=<your key>
AZURE_OPENAI_ENDPOINT=https://<your-resource>.services.ai.azure.com/openai/v1
AZURE_OPENAI_DEPLOYMENTS=gpt-5.4-nano,gpt-5.6-sol
```

`.env` is gitignored and is the only copy of your key -- keep a backup
somewhere outside the repo.

### Switching models

The sidebar picker is driven by `AZURE_OPENAI_DEPLOYMENTS`. The **first name
is the default selection**. Add a model by appending its deployment name and
refreshing the page; the value is re-read on every run, so no restart is
needed. Whitespace and duplicates are ignored.

Names must match the deployment names in the Azure AI Foundry portal exactly
-- a mismatch surfaces as a 404, and the app says so. Note the endpoint
advertises Azure's entire catalog (400+ models), but a resource only serves
what is actually deployed on it.

## Running

```bash
streamlit run app.py
```

Opens at http://localhost:8501.

`test_azure_api.py` is a non-UI smoke test that checks the endpoint answers:

```bash
python test_azure_api.py
```

## Deploying to Streamlit Community Cloud

1. Push to GitHub (see below).
2. At https://share.streamlit.io, click **Create app** and point it at this
   repo, branch `main`, main file `app.py`.
3. Open **Advanced settings > Secrets** and paste the three values in TOML
   form -- see `.streamlit/secrets.toml.example`:

   ```toml
   AZURE_OPENAI_API_KEY = "your-key-here"
   AZURE_OPENAI_ENDPOINT = "https://your-resource.services.ai.azure.com/openai/v1"
   AZURE_OPENAI_DEPLOYMENTS = "gpt-5.4-nano,gpt-5.6-sol"
   ```

4. Deploy.

`config.py` reads environment variables first, then `.env`, then Streamlit
secrets, so the same code runs locally and deployed with no changes.

**Before deploying, note:** a deployed app is reachable by anyone with the
URL and calls Azure with *your* key, so every visitor spends your quota.
Streamlit Cloud has no built-in auth on the free tier. Keep the app private,
or add a password gate, or use a key with a low spending cap.

## Pushing changes

```bash
git add -A
git commit -m "your message"
git push
```

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI |
| `config.py` | Settings (env / .env / Streamlit secrets) and the Azure client |
| `doc_text.py` | PDF, DOCX and plain-text extraction |
| `test_azure_api.py` | Non-UI endpoint smoke test |
| `.streamlit/config.toml` | Upload size limit |
