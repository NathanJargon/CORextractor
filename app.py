from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_with_special_chars(pdf_file):
    images = convert_from_path(pdf_file)
    text_lines = []

    for img in images:
        text = pytesseract.image_to_string(img, lang='eng', config='--psm 12')

        for line in text.split("\n"):
            if line.strip():
                text_lines.append(line) 

    return text_lines

def add_page_numbers(text): # debug purposes
    lines = text.split('\n')
    text_with_page_numbers = ""

    for page_number, line in enumerate(lines, start=1):
        text_with_page_numbers += f" Page {page_number} | {line}\n"

    return text_with_page_numbers
    #return lines

def extract_info(text):
    info_dict = {
        "Id": text[15],
        "Name": text[18],
        "Campus": text[9],
        "Gender": text[21],
        "Age": text[27],
        "College": text[16].split(": ")[-1],
        "Department/Program": text[19].split(": ")[-1],
        "Major": text[24],
        "Year-Level": text[29].split(": ")[-1],
        "Curriculum": text[25].split(": ")[-1],
        "Scholarship": text[30].split(":")[-1] if len(text[30].split(":")[-1]) > 0 else "N/A",
        "Nationality": text[22].split(":")[-1],
        "Contact": text[28].split(" ")[-1] if len(text[28].split(" ")[-1]) > 1 else "N/A",
        "Document-Title": text[3],
        "Registration-Number": text[10],
        "Academic-Year": text[13].split(": ")[-1],
    }
    
    return info_dict
    

if __name__ == "__main__":
    pdf_file = "COR.pdf"
    extracted_text = extract_text_with_special_chars(pdf_file)
    #text_with_page_numbers = add_page_numbers(extracted_text)
    info = extract_info(extracted_text)
    #print(extracted_text)
    for key, value in info.items():
        print(f"{key}: {value}")
