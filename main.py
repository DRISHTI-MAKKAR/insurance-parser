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

    # Step 4: Combine prompt with extracted PDF text
    final_prompt = f"""
    Document text:{extracted_text}
    User instruction:{user_prompt}
"""

    # Step 5: Send to Claude
    response = ask_claude(final_prompt)

    # Step 6: Print response
    print("\nClaude Response:")
    print(response)


if __name__ == "__main__":
    main()