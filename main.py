import json
import os

from pdf_reader import read_pdf
from claude_client import ask_claude


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


    # Step 4: Combine PDF text and user instruction
    final_prompt = f"""
Here is the insurance document:

--------------------
{extracted_text}
--------------------

User instruction:
{user_prompt}

Return the response only in valid JSON format.
"""


    # Step 5: Send request to Claude
    response = ask_claude(final_prompt)


    # Step 6: Convert Claude response into JSON
    try:
        json_data = json.loads(response)

    except json.JSONDecodeError:
        print("Claude did not return valid JSON.")
        print("\nClaude Response:")
        print(response)
        return


    # Step 7: Display only current prompt output
    print("\nClaude Response:")
    print(json.dumps(json_data, indent=4))


    # Step 8: Store all prompt outputs in JSON file
    file_name = "insurance_output.json"


    # Check if JSON history file already exists
    if os.path.exists(file_name):

        with open(file_name, "r") as file:
            history = json.load(file)

    else:
        history = []


    # Add current prompt and response
    history.append(
        {
            "prompt": user_prompt,
            "response": json_data
        }
    )


    # Save updated history
    with open(file_name, "w") as file:
        json.dump(history, file, indent=4)


    print("\nResponse saved to insurance_output.json")


if __name__ == "__main__":
    main()