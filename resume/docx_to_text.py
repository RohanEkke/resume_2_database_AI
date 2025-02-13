import docx2txt



def docx_to_text(file_path):
    try:
        # Extract text from the .docx file
        text = docx2txt.process(file_path)
        extracted_text = "\n".join([line for line in text.splitlines() if line.strip()])
        # Validation: Check if text was extracted
        if not extracted_text.strip():
            return "Error: No text found in the .docx file."
        
        return extracted_text
    
    except Exception as e:
        return f"Error: An unexpected error occurred - {e}"

# Example usage
# file_path = input("Enter the path to your .docx file: ")

