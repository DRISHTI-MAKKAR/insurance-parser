import json

from pdf_reader import read_pdf
from claude_client import ask_claude
from json_utils import (
    parse_json_response,
    save_json,
    verify_field
)


def main():

    # Step 1: Get PDF path from user
    pdf_path = input("Enter PDF path: ")

    # Step 2: Extract text from PDF
    extracted_text = read_pdf(pdf_path)

    if extracted_text is None:
        print("Could not extract text from PDF.")
        return

    # Step 3: Get multi-line user prompt
    print("\nEnter your prompt.")
    print("Type END on a new line when you are finished:\n")

    prompt_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        prompt_lines.append(line)

    user_prompt = "\n".join(prompt_lines)

    # Step 4: Create final prompt
    final_prompt = f"""
Here is the insurance document:
--------------------
{extracted_text}
--------------------

User instruction:
{user_prompt}

Rules:
- Return only valid JSON.
- If any field is missing, return null.
- Do not omit fields.
"""

    # Step 5: Send request to Claude
    response = ask_claude(final_prompt)

    # Display token usage
    print("\nToken Usage:")
    print(f"Input Tokens : {response['input_tokens']}")
    print(f"Output Tokens: {response['output_tokens']}")
    print(f"Total Tokens : {response['input_tokens'] + response['output_tokens']}")

    # Step 6: Parse Claude JSON response
    json_data = parse_json_response(response["output"])

    if json_data is None:
        print("Claude did not return valid JSON.")
        print("\nClaude Response:")
        print(response["output"])
        return

    # Step 7: Verify all extracted fields
    print("\nVerification:")

    all_verified = True

    for key, value in json_data.items():

        verified = verify_field(value, extracted_text)

        if verified:
            print(f"{key} verified successfully.")
        else:
            print(f"{key} verification failed! Value not found in the source document.")
            all_verified = False

    if all_verified:
        print("\nAll fields verified successfully.")
    else:
        print("\nSome fields could not be verified.")

    # Step 8: Display Claude response
    print("\nClaude Response:")
    print(json.dumps(json_data, indent=4))

    # Step 9: Save response history
    output_path = r"C:\Users\makka\OneDrive\Documents\output\insurance_output.json"

    save_json(
        json_data,
        user_prompt,
        output_path
    )

    print("\nResponse saved successfully!")


if __name__ == "__main__":
    main()