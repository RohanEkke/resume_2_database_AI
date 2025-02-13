import pdfplumber
import re


# Example usage:


def pdf_to_text(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    cleaned_text = re.sub(r"(?:•|·|●|▪|■|◆|◦|▶|☛|✦|➤|➔|➢|➡|⇒|→|\*)", "", page_text)
                    remove_o = re.sub(r"^\s*o\s+", "", cleaned_text, flags=re.MULTILINE)
                    text += remove_o +'\n'
            return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


