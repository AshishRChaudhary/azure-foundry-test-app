from openai import OpenAI

import config

client = OpenAI(
    base_url=config.AZURE_OPENAI_ENDPOINT,
    api_key=config.AZURE_OPENAI_API_KEY,
)

response = client.responses.create(
    model=config.default_deployment(),
    input="What is the capital of France?",
)

print(f"answer: {response.output[0]}")
