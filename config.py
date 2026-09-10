"""Settings and the Azure client.

Everything configurable lives in .env: the endpoint, the API key, and the
comma-separated list of deployment names shown in the model picker.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load the .env sitting next to this file, not relative to the current
# working directory -- so the app works no matter where it's run from.
load_dotenv(Path(__file__).with_name(".env"))


def get(name: str, default: str | None = None) -> str:
    """Return a setting, or raise if it's missing and has no default."""
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(
            f"{name} is not set. Add it to .env (see .env.example)."
        )
    return value


def deployments() -> list[str]:
    """Deployment names from AZURE_OPENAI_DEPLOYMENTS, in order.

    Read fresh on each call so edits to .env show up on a page refresh.
    """
    raw = get("AZURE_OPENAI_DEPLOYMENTS")
    names = []
    for name in raw.split(","):
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


AZURE_OPENAI_API_KEY = get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = get("AZURE_OPENAI_ENDPOINT")
