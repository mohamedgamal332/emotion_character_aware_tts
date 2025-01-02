input_dir = "../in/"
output_dir = "../temp/"

# Convert pdf to text
import re
import os
from PyPDF2 import PdfReader

def process_pdf(file_path):
    # Read the PDF
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        # Extract text from each page and remove unnecessary white spaces
        text = page.extract_text()
        text = re.sub(r"(\s*-\s*\n|\s*\n\s*)", " ", text)  # Handle hyphenations and line breaks
        text = re.sub(r"\s+", " ", text).strip()           # Remove extra spaces
        full_text += text + " "

    # Save each part as a separate text file
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + ".txt"), "w", encoding="utf-8") as f:
        # Write the file name at the beginning of each part
        f.write(full_text)

    print(f"Processed and saved {os.path.basename(file_path)}")

def process_directory(input_dir):
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(input_dir, file_name)
            process_pdf(file_path)

process_directory(input_dir)