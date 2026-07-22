import json
import os


def clean_json_response(response):
    """
    Remove markdown code fences added by the LLM.
    Example:
    ```json
    {...}
    ```
    becomes:
    {...}
    """

    response = response.replace("```json", "")
    response = response.replace("```", "")

    return response.strip()


def parse_json_response(response):
    """
    Convert Claude response string into Python dictionary.
    """

    cleaned_response = clean_json_response(response)

    try:
        return json.loads(cleaned_response)

    except json.JSONDecodeError:
        return None


def save_json(data, prompt, file_path):
    """
    Store all prompts and responses in JSON file.
    """

    if os.path.exists(file_path):

        with open(file_path, "r") as file:
            history = json.load(file)

    else:
        history = []

    history.append(
        {
            "prompt": prompt,
            "response": data
        }
    )

    with open(file_path, "w") as file:
        json.dump(history, file, indent=4)


def verify_field(value, source_text):
    """
    Verify that an extracted field exists exactly
    in the original source text.

    Returns:
        True  -> if verified
        False -> if not verified
    """

    # If Claude returned null, verification succeeds.
    if value is None:
        return True

    # Convert non-string values (numbers, etc.) to string.
    value = str(value)

    # Check whether the extracted value exists in the source text.
    return value in source_text