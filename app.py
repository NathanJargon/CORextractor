import psycopg2
from pdf2image import convert_from_path
import pytesseract

# Set up PostgreSQL connection parameters
db_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'admin',
    'port': '5432'
}

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def record_exists(cursor, id_value):
    # Check if the record with the given ID exists in the database
    cursor.execute("SELECT id FROM student_info WHERE id = %s;", (id_value,))
    existing_record = cursor.fetchone()
    print(f"Existing Record: {existing_record}")
    return existing_record is not None

def insert_into_database(info_dict):
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Check if the record already exists
        if record_exists(cursor, info_dict['Id']):
            print(f"Record with ID {info_dict['Id']} already exists. Skipping insertion.")
        else:
            # Insert information into the database
            cursor.execute("""
                INSERT INTO student_info (
                    id, name, campus, gender, age, college, department, major, year_level,
                    curriculum, scholarship, nationality, contact, document_title, registration_number, academic_year
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                info_dict['Id'], info_dict['Name'], info_dict['Campus'], info_dict['Gender'], info_dict['Age'],
                info_dict['College'], info_dict['Department/Program'], info_dict['Major'], info_dict['Year-Level'],
                info_dict['Curriculum'], info_dict['Scholarship'], info_dict['Nationality'], info_dict['Contact'],
                info_dict['Document-Title'], info_dict['Registration-Number'], info_dict['Academic-Year']
            ))
            # Commit the transaction
            conn.commit()

    except Exception as e:
        print(f"Error inserting into database: {e}")

    finally:
        # Close the database connection and cursor
        if conn:
            conn.close()
        if cursor:
            cursor.close()
            
            
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

def retrieve_from_database():
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Fetch information from the database
        cursor.execute("""
            SELECT * FROM student_info
        """)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        return rows

    except Exception as e:
        print(f"Error retrieving from database: {e}")

    finally:
        # Close the database connection and cursor
        if conn:
            conn.close()
        if cursor:
            cursor.close()
            
def retrieve_single_record_from_database(id_value):
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Fetch information for the specific ID
        cursor.execute("""
            SELECT * FROM student_info WHERE id = %s;
        """, (id_value,))

        # Fetch the row from the result set
        row = cursor.fetchone()

        return row

    except Exception as e:
        print(f"Error retrieving from the database: {e}")

    finally:
        # Close the database connection and cursor
        if conn:
            conn.close()
        if cursor:
            cursor.close()
            
if __name__ == "__main__":
    pdf_file = "test-file/cor.pdf"
    extracted_text = extract_text_with_special_chars(pdf_file)
    info = extract_info(extracted_text)

    # Insert into PostgreSQL database
    insert_into_database(info)

    # Print inserted data
    print("Inserted data:")
    for key, value in info.items():
        print(f"{key}: {value}")

    print("\nRetrieved data:")
    
    # Retrieve data for the specific ID from PostgreSQL database
    retrieved_data = retrieve_single_record_from_database(info['Id'])

    # Print retrieved data
    print(retrieved_data)