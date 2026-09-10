"""Settings and the Azure client.

Configuration comes from, in order of precedence:

1. Real environment variables
2. A local .env file (used when running on your own machine)
3. Streamlit secrets (used when deployed to Streamlit Community Cloud,
   which has no .env -- you paste the same keys into the app's Secrets box)

So the same code runs locally and deployed with no changes.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load the .env sitting next to this file, not relative to the current
# working directory -- so the app works no matter where it's run from.
load_dotenv(Path(__file__).with_name(".env"))


def _from_streamlit_secrets(name: str) -> str | None:
    """Look name up in st.secrets, or None if unavailable.

    Wrapped because st.secrets raises when there is no secrets file at
    all, which is the normal case for a plain local run.
    """
    try:
        import streamlit as st

        return st.secrets[name]
    except Exception:
        return None


def get(name: str, default: str | None = None) -> str:
    """Return a setting, or raise if it's missing and has no default."""
    value = os.getenv(name) or _from_streamlit_secrets(name) or default
    if value is None or value == "":
        raise RuntimeError(
            f"{name} is not set. Locally, add it to .env (see .env.example). "
            "On Streamlit Community Cloud, add it under Settings > Secrets."
        )
    return value


def deployments() -> list[str]:
    """Deployment names from AZURE_OPENAI_DEPLOYMENTS, in order.

    Read fresh on each call so config edits show up on a page refresh.
    """
    names = []
    for name in get("AZURE_OPENAI_DEPLOYMENTS").split(","):
        name = name.strip()
        if name and name not in names:
            names.append(name)
    if not names:
        raise RuntimeError(
            "AZURE_OPENAI_DEPLOYMENTS is empty. Set it to a comma-separated "
            "list of deployment names, e.g. gpt-5.4-nano,gpt-5.6-sol"
        )
    return names


def default_deployment() -> str:
    """The first name in AZURE_OPENAI_DEPLOYMENTS."""
    return deployments()[0]


def client(timeout: float = 60.0) -> OpenAI:
    """An OpenAI client pointed at the Azure endpoint."""
    return OpenAI(
        base_url=get("AZURE_OPENAI_ENDPOINT"),
        api_key=get("AZURE_OPENAI_API_KEY"),
        timeout=timeout,
    )
