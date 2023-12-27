import os
import fitz  # PyMuPDF library

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)  # Open the PDF file
    all_text = ""

    for page in doc:
        all_text += page.get_text() + chr(12)

    # Replace typographic quotation marks
    output_string = all_text.replace('“', '"')
    # Replace typographic quotation marks
    final_string = output_string.replace('”', '"')
    # Replace new line characters
    final_final_string = final_string.replace("\n", " ")
    # Replace typographic apostrophes
    ultimate_string = final_final_string.replace("’", "'")
    # Remove common ligatures with their respective characters
    the_string = ultimate_string.replace("ﬁ", "fi")
    # Remove extra spaces and trailing spaces
    the_string = ' '.join(the_string.split())

    return the_string


def main():
    # Specify the folder path containing the PDF files
    folder_path = 'Files'
    output_file_path = 'data/aequitas_content.tsv'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Iterate through all PDF files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                pdf_file_path = os.path.join(folder_path, filename)
                extracted_text = extract_text_from_pdf(pdf_file_path)
                output_file.write(f"{extracted_text}\n")
           
            
                # You can do something with the extracted text here, such as saving it to a file or processing it further
                # For now, let's print the text for each file
                print(f"Text extracted from {filename}")
    subprocess.run(['python3', 'abstract-extractor.py'])

if __name__ == "__main__":
    main()