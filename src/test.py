import mysql.connector
import csv
from mysql.connector import Error

# --- Database Configuration (same as above) ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'admin',
    'database': 'ssis'
}


def import_data_from_csv(file_path, table):
    """Imports colleges from a CSV file into the database."""
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Open the CSV file
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row if present

            # Insert each row into the colleges table
            sql = f"INSERT IGNORE INTO {table} (student_id, first_name, last_name, sex, year_level, college_code, program_code) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            for row in csv_reader:
                cursor.execute(sql, (row[3], row[0], row[1], row[2], row[4], row[5], row[6]))

        # Commit the transaction
        connection.commit()
        print(f"Successfully imported colleges from {file_path}")

    except Error as e:
        print(f"Error importing colleges: {e}")
        if connection:
            connection.rollback()  # Roll back changes on error
            print("Transaction rolled back.")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def insert_data(data, table):
    query = None
    if table == "colleges":
        query = "(college_code, college_name) VALUES (%s, %s)"
    elif table == "programs":
        query = "(college_code, program_code, program_name) VALUES (%s, %s, %s)"
    elif table == "students":
        query = "(student_id, first_name, last_name, sex, year_level, college_code, program_code) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(f"INSERT IGNORE INTO {table} {query}", data)
        connection.commit()

    except Error as e:
        print(f"Error importing colleges: {e}")
        if connection:
            connection.rollback()  # Roll back changes on error
            print("Transaction rolled back.")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# --- Example Usage ---
if __name__ == "__main__":
    # Data for the new student as a tuple
    # Ensure data types match the table definition (VARCHAR, ENUM, etc.)
    # Make sure 'CCS' and 'BSCS' exist in the 'programs' table first!
    csv_file_path = "./database/students.csv"  # Replace with the path to your CSV file
    import_data_from_csv(csv_file_path, "students")


