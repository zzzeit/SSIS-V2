import json
import csv
import os
import sqlite3 as sql
import datetime
import tkinter as tk
from tkinter import messagebox as tk_messagebox

# COLLEGES
CNAME_ = 0
CCODE_ = 1
# PROGRAMS
ccode = 0
pcode = 1
pname = 2
# STUDENTS
FNAME = 0
LNAME = 1
SEX = 2
ID = 3
YRLVL = 4
CCODE = 5
PCODE = 6

def write_data(filename, data, int=0):
    v = ["fname","lname","sex","ID#","year lvl","college code","program code"]
    if int == 1:
        v = ["College","Program Code","Program Name"]
    elif int == 2:
        v = ["College Name", "College Code"]
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(v)
        writer.writerows(data)
def load_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        return list(reader)
    



def printTime(message):
    """ print the current time with a message """
    now = datetime.datetime.now()
    print(f"[{now.strftime("%H:%M:%S.") + f"{int(now.microsecond/1000):03d}"}]  {message}")


class DataManager:
    def __init__(self, db_name='./database/database.db'):
        self.db_name = db_name
        self.conn = sql.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self):
        """Create tables in the database if they do not exist."""

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS colleges (
            college_name TEXT,
            college_code TEXT PRIMARY KEY
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS programs (
            college_code TEXT,
            program_code TEXT PRIMARY KEY,
            program_name TEXT,
            FOREIGN KEY (college_code) REFERENCES colleges(college_code) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
            fname TEXT,
            lname TEXT,
            sex TEXT,
            ID TEXT PRIMARY KEY,
            year_lvl TEXT,
            college_code TEXT,
            program_code TEXT,
            FOREIGN KEY (college_code) REFERENCES colleges(college_code) ON DELETE CASCADE,
            FOREIGN KEY (program_code) REFERENCES programs(program_code) ON DELETE CASCADE
            )
        ''')

    # -------------------------------------------------------------------------------------------------------- STUDENTS
    def insert_student(self, student_data):
        """Insert a new student into the database."""
        try:
            self.cursor.execute('''
                INSERT INTO students (fname, lname, sex, ID, year_lvl, college_code, program_code)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', student_data)
            self.conn.commit()
        except Exception as e:
            printTime(f"Error inserting student: {e}")

    def get_students(self):
        """Retrieve all students from the database."""
        try:
            self.cursor.execute('SELECT * FROM students')
            return self.cursor.fetchall()
        except Exception as e:
            printTime(f"Error retrieving students: {e}")
            return []

    def get_student_by_id(self, student_id):
        """Retrieve a student by their ID."""
        try:
            self.cursor.execute('SELECT * FROM students WHERE ID = ?', (student_id,))
            return self.cursor.fetchone()
        except Exception as e:
            printTime(f"Error retrieving student by ID: {e}")
            return None


    # -------------------------------------------------------------------------------------------------------- PROGRAMS
    def insert_program(self, program_data):
        """Insert a new program into the database."""
        try:
            self.cursor.execute('''
                INSERT INTO programs (college_code, program_code, program_name)
                VALUES (?, ?, ?)
            ''', program_data)
            self.conn.commit()
        except Exception as e:
            printTime(f"Error inserting program: {e}")

    def get_programs(self):
        """Retrieve all programs from the database."""
        try:
            self.cursor.execute('SELECT * FROM programs')
            return self.cursor.fetchall()
        except Exception as e:
            printTime(f"Error retrieving programs: {e}")
            return []

    # -------------------------------------------------------------------------------------------------------- COLLEGES
    def insert_college(self, college_data):
        """Insert a new college into the database."""
        try:
            self.cursor.execute('''
                INSERT INTO colleges (college_name, college_code)
                VALUES (?, ?)
            ''', college_data)
            self.conn.commit()
        except Exception as e:
            printTime(f"Error inserting college: {e}")
    
    def get_colleges(self):
        """Retrieve all colleges from the database."""
        try:
            self.cursor.execute('SELECT * FROM colleges')
            return self.cursor.fetchall()
        except Exception as e:
            printTime(f"Error retrieving colleges: {e}")
            return []
        
    def delete_college(self, college_code):
        """Delete a college from the database."""
        try:
            self.cursor.execute('''
                DELETE FROM colleges
                WHERE college_code = ?
            ''', (college_code,))
            self.conn.commit()
        except Exception as e:
            printTime(f"Error deleting college: {e}")

    def update_college(self, college_code, new_name):
        """Update the name of a college."""
        try:
            self.cursor.execute('''
                UPDATE colleges
                SET college_name = ?
                WHERE college_code = ?
            ''', (new_name, college_code))
            self.conn.commit()
        except Exception as e:
            printTime(f"Error updating college: {e}")
    

    def close(self):
        """Close the database connection."""
        self.conn.close()