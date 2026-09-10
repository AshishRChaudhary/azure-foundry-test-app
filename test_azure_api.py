"""Smoke test: does the configured endpoint answer?"""

import config

response = config.client().responses.create(
    model=config.default_deployment(),
    input="What is the capital of France?",
)

print(f"answer: {response.output[0]}")
