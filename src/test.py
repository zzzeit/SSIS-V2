import csv
from data_management import DataManager

if __name__ == "__main__":
    DB = DataManager()

    # Insert all colleges from colleges.csv
    with open("./database/colleges.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            # row: [College Name, College Code]
            DB.insert_college(row)

    # Insert all programs from programs.csv
    with open("./database/programs.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            # row: [College, Program Code, Program Name]
            DB.insert_program(row)

    # Insert all students from students.csv
    with open("./database/students.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            DB.insert_student(row)



    DB.close()