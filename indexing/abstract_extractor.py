import os
import fitz  # PyMuPDF library

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file, max_characters=400):
    doc = fitz.open(pdf_file)
    extracted_text = ""

    for page in doc:
        text = page.get_text() + chr(12)
        if len(extracted_text) + len(text) <= max_characters:
            extracted_text += text
        else:
            remaining_characters = max_characters - len(extracted_text)
            extracted_text += text[:remaining_characters]
            break

    output_string = extracted_text.replace('“', '"')
    final_string = output_string.replace('”', '"')
    final_final_string = final_string.replace("\n", " ")
    ultimate_string = final_final_string.replace("’", "'")
    the_string = ultimate_string.replace("ﬁ", "fi")
    the_string = ' '.join(the_string.split())
    
    return the_string

def main():
    # Specify the folder path containing the PDF files
    folder_path = 'Files'
    BASE_PATH = '/Users/penel/Downloads/dropbox-solr/'
    output_file_path = f'{BASE_PATH}/data/aequitas_abstract.tsv'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Iterate through all PDF files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                print(filename)
                pdf_file_path = os.path.join(folder_path, filename)
                extracted_text = extract_text_from_pdf(pdf_file_path)
                output_file.write(f"{extracted_text}\n")


if __name__ == "__main__":
    main()