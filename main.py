import json

from pdf_reader import read_pdf
from claude_client import ask_claude
from json_utils import parse_json_response, save_json


def main():

    # Step 1: Get PDF path from user
    pdf_path = input("Enter PDF path: ")


    # Step 2: Extract text from PDF
    extracted_text = read_pdf(pdf_path)

    if extracted_text is None:
        print("Could not extract text from PDF.")
        return


    # Step 3: Get user prompt
    user_prompt = input("\nEnter your prompt: ")


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


    # Step 6: Parse Claude JSON response
    json_data = parse_json_response(response)


    if json_data is None:
        print("Claude did not return valid JSON.")
        print("\nClaude Response:")
        print(response)
        return


    # Step 7: Display current response only
    print("\nClaude Response:")
    print(json.dumps(json_data, indent=4))


    # Step 8: Save response history
    output_path = r"C:\Users\makka\OneDrive\Documents\output\insurance_output.json"


    save_json(
        json_data,
        user_prompt,
        output_path
    )


    print("\nResponse saved successfully!")


if __name__ == "__main__":
    main()