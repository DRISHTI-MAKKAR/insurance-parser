import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def ask_claude(user_prompt):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,

        system="""
You are an expert insurance document extraction assistant.

Your job is to extract information accurately from insurance documents.

Rules:
- Follow the user's instructions exactly.
- If asked to return JSON, return ONLY valid JSON.
- Never invent information.
- If a requested field is missing, return null.
- Do not include explanations unless explicitly requested.
""",

        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return {
        "output": response.content[0].text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens
    }