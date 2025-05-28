import tkinter as tk
from math import ceil
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from data_management import *

import main

class MiniProfile:
    def __init__(self, app, master, list_element):
        frame = tk.Frame(master, bg=app.getColor(2), width=620, height=30)
        frame.pack_propagate(False)
        frame.pack(pady=5, padx=10)
        if app.list_mode == 0:
            frame.bind("<Button-1>", lambda event: [app.setMainStud(list_element), app.transition_frames(app.frame2_obj)])
            for i in range(0, len(list_element)):
                t = list_element[i]
                if i == ID:
                    t = text=str(list_element[ID])[:4] + "-" + str(list_element[ID])[4:8]
                l = tk.Label(frame, text=t, bg=app.getColor(2), width=11)
                l.pack_propagate(False)
                l.pack(padx=(3, 0), side="left")
                l.bind("<Button-1>", lambda event: [app.setMainStud(list_element), app.transition_frames(app.frame2_obj)])
            
        elif app.list_mode == 1:
            frame.bind("<Button-1>", lambda event: [app.setMainProg(list_element), app.transition_frames(app.frame_edit_program_obj)])
            for i in range(0, len(list_element)):
                t = list_element[i]
                w = 11
                if i == 2:
                    w = 70
                l = tk.Label(frame, text=t, bg=app.getColor(2), width=w)
                l.pack_propagate(False)
                l.pack(padx=(3, 0), side="left")
                l.bind("<Button-1>", lambda event: [app.setMainProg(list_element), app.transition_frames(app.frame_edit_program_obj)])

        elif app.list_mode == 2:
            frame.bind("<Button-1>", lambda event: [app.setMainColl(list_element), app.transition_frames(app.frame_edit_college_obj)])
            for i in range(0, len(list_element)):
                t = list_element[i]
                w = 70
                if i == 1:
                    w = 10
                l = tk.Label(frame, text=t, bg=app.getColor(2), width=w)
                l.pack_propagate(False)
                l.pack(padx=(3, 0), side="left")
                l.bind("<Button-1>", lambda event: [app.setMainColl(list_element), app.transition_frames(app.frame_edit_college_obj)])

class Frame1: # CRUDL FRAME
    def __init__(self, app):
        self.app = app
        self.entry_str_var = tk.StringVar()
        self.entry_str_var.trace_add(mode="write", callback=self.on_entry_updated)
        self.acquired_list = app.students_database
        self.page = 1
        self.maxPage = ceil(len(self.acquired_list)/12)

        self.stud_label = {"First N":43, "Last N":47, "Sex":55, "ID#":66, "Year Level":43, "College":35, "Code":45}
        self.col_label = {"College":43, "Program Code":28, "Program Name": 185}

        self.create_widgets(app)

    def create_widgets(self, app):
        self.frame1 = tk.Frame(app.getRoot(), width=682.5, height=640, bg=self.app.getColor(0))
        self.frame1.pack_propagate(False)

        self.top_frame = tk.Frame(master=self.frame1, width=665, height=50, bg=app.getColor(0))
        self.top_frame.pack_propagate(False)
        self.top_frame_container = tk.Frame(self.top_frame, bg=app.getColor(0))
        self.search_entry = ttk.Entry(master=self.top_frame_container, width=30, font=("Helvetica", 15), textvariable=self.entry_str_var)
        self.top_frame_container.pack()
        self.top_frame.pack(pady=(20,0))

        self.add_student_button = ttk.Button(self.top_frame_container, width=5, text="Add", command=lambda: self.add_button_func())
        self.settings_button = ttk.Button(self.top_frame_container, text="Settings", command=lambda: app.transition_frames(app.frame4_obj))
        self.add_student_button.pack(side="left")
        self.search_entry.pack(side="left", padx=100)
        self.settings_button.pack(side="left")

        self.top_row_frame = tk.Frame(master=self.frame1, width=665 , height=25, bg=app.getColor(2))
        self.top_row_frame.pack_propagate(False)
        self.top_row_frame.pack(pady=(10, 15))

        self.labels_frame = tk.Frame(master=self.top_row_frame, bg=app.getColor(2))
        self.labels_frame.pack(padx=(0, 10), side="left")

        self.label_frame_upd(0)
            
        

        self.bot_frame = tk.Frame(master=self.frame1, width=665, height=480, bg=app.getColor(1))
        self.bot_frame.pack_propagate(False)
        self.bot_frame.pack()

        # Page Number
        self.page_frame = tk.Frame(master=self.frame1, width=50, height=30, bg=app.getColor(2))
        self.page_label2_var = tk.StringVar()
        self.page_entry_var = tk.StringVar()
        self.page_entry_var.trace_add("write", callback=self.page_entry_upd)
        self.page_frame.pack(side="top", pady=5)

        self.prev_button = ttk.Button(master=self.page_frame, width=1, text="<", command=self.prev_page)
        self.next_button = ttk.Button(master=self.page_frame, width=1, text=">", command=self.next_page)
        self.page_label1 = tk.Label(master=self.page_frame, text="Page", bg=app.getColor(2))
        self.page_label2 = tk.Label(master=self.page_frame, bg=app.getColor(2), textvariable=self.page_label2_var)
        self.page_entry = ttk.Entry(master=self.page_frame, width=3, textvariable=self.page_entry_var, justify="center")
        
        self.prev_button.pack(side="left")
        self.page_label1.pack(side="left", padx=3)
        self.page_entry.pack(side="left")
        self.page_label2.pack(side="left", padx=3)
        self.next_button.pack(side="left")


        self.page_label2_var.set(f"of {self.maxPage}")
        self.page_entry_var.set("1")


    def on_entry_updated(self, *args):
        if not self.entry_str_var.get():
            self.show_list()
            return 0

        for widget in self.bot_frame.winfo_children():
            widget.pack_forget()

        SEARCH_TYPE = self.app.getSearchSet()
        temp = []
        for student in self.acquired_list:
            match = True
            for i, letter in enumerate(self.entry_str_var.get()):
                if i >= len(student[SEARCH_TYPE]) or letter.upper() != student[SEARCH_TYPE][i].upper():
                    match = False
                    break
            if match:
                temp.append(student)

   
        for student in temp:
            MiniProfile(self.app, self.bot_frame, student)

    def add_button_func(self):
        self.app.transition_frames(self.app.frame3_obj)
    def page_entry_upd(self, *args):
        ev = self.page_entry_var.get() # entry value
        if ev.isnumeric():
            if (int(ev) >= 1 and int(ev) <= self.maxPage):
                self.page = int(ev)
            else:
                self.page = 1
                self.page_entry_var.set("1")
            self.show_list()

    def label_frame_upd(self, int_label):

        if int_label == 0:
            labels = self.stud_label
        elif int_label == 1:
            labels = self.col_label
        for i in self.labels_frame.winfo_children():
            i.pack_forget()
        for i in list(labels.keys()):
            self.label_ = tk.Label(master=self.labels_frame, bg=self.app.getColor(2), text=i)
            self.label_.pack(side="left", padx=(labels[i],0))

    def show_list(self):
        for widget in self.bot_frame.winfo_children():
            widget.pack_forget()
        if self.app.filter_mode != None:
            self.filter_list()
        if self.app.list_mode == 0:
            self.add_student_button.configure(command=lambda: self.app.transition_frames(self.app.frame3_obj))
        elif self.app.list_mode == 1:
            self.add_student_button.configure(command=lambda: self.app.transition_frames(self.app.frame5_obj))
        self.maxPage = ceil(len(self.acquired_list)/12)
        self.page_label2_var.set(f"of {self.maxPage}")
        for i in range((self.page - 1) * 12, self.page * 12):
            if i < len(self.acquired_list):
                MiniProfile(self.app, self.bot_frame, self.acquired_list[i])

    def filter_list(self):
        temp = []
        try:
            for i in self.acquired_list:
                if i[self.app.filter_mode] == self.app.filter_value:
                    temp.append(i)
            self.acquired_list = temp
        except:
            pass


    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.show_list()
            self.page_entry_var.set(f"{self.page}")

    def next_page(self):
        if self.page < self.maxPage:
            self.page += 1
            self.show_list()
            self.page_entry_var.set(f"{self.page}")

    def go_to_page(self, page):
        if page > 0 and page <= self.maxPage:
            self.page = page
            self.show_list()
            self.page_entry_var.set(f"{self.page}")

    def transition(self):
        self.page = 1
        self.page_entry_var.set("1")
        self.frame1.pack()
        if self.app.list_mode == 0:
            self.acquired_list = self.app.students_database
            self.label_frame_upd(0)
        elif self.app.list_mode == 1:
            self.acquired_list = self.app.getProgramDb()
            self.label_frame_upd(1)
        self.show_list()


    def getMainFrame(self):
        return self.frame1

class Frame2:
    def __init__(self, app):
        self.app = app
        self.frame2 = tk.Frame(app.getRoot(), width=682.5, height=590, bg=app.getColor(0))
        self.frame2.pack_propagate(False)
        # self.frame2.pack()

        self.header = tk.Frame(self.frame2, width=682.5, height=50, bg=app.getColor(0))
        self.header.pack_propagate(False)
        self.header.pack()

        self.back_button = ttk.Button(self.header, text="Back", width=5, command=lambda: [app.transition_frames(app.frame1_obj), app.setMainStud(None)])
        self.back_button.pack(side="left", padx=10)

        self.delete_button = ttk.Button(self.header, text="Delete", width=6, command=lambda: [app.delete_student(app.getMainStud()[ID]), app.transition_frames(app.frame1_obj)])
        self.delete_button.pack(side="right", padx=10)

        self.edit_button = ttk.Button(self.header, text="Edit", width=6, command=lambda: [app.transition_frames(app.frame6_obj), app.setMainStud(app.getMainStud())])
        self.edit_button.pack(side="right", padx=10)

        self.body1 = tk.Frame(self.frame2, width=682.5, height=300, bg=app.getColor(0))
        self.body1.pack_propagate(False)
        self.body1.pack()

        # Image PFP
        self.canvas2 = tk.Canvas(self.body1, width=175, height=175, highlightthickness=0)
        self.canvas2.pack(pady=20)

        image = Image.open("./assets/image.jpg")
        image = image.resize((175, 175))
        photo = ImageTk.PhotoImage(image)

        self.canvas2.create_image(87.5, 87.5, image=photo, anchor=tk.CENTER)
        self.canvas2.image = photo  # Keep a reference to avoid garbage collection

        self.canvas2.create_oval(-50, -50, 225, 225, outline=app.getColor(0), width=100)

        self.nameFrame = tk.Frame(self.body1, bg=app.getColor(0))
        self.nameFrame.pack()
        # Full Name
        self.full_name_var = tk.StringVar(value="Empty")
        self.full_name = tk.Label(self.nameFrame, textvariable=self.full_name_var, font=("Helvetica", 16), bg=app.getColor(0), foreground="white")
        self.full_name.pack()

        # ID Number
        self.id_var = tk.StringVar(value="0000-0000")
        self.id = tk.Label(self.nameFrame, textvariable=self.id_var, font=("Helvetica", 10), bg=app.getColor(0), foreground="white")
        self.id.pack()

        # Border
        self.border = tk.Canvas(self.body1, width=340, height=10, highlightthickness=0, bg=app.getColor(0))
        self.border.pack(side="bottom")

        self.border.create_line(0, 5, 340, 5, width=3, fill=app.getColor(3))

        # BODY 2
        self.body2 = tk.Frame(self.frame2, width=682.5, height=250, bg=app.getColor(0))
        self.body2.pack_propagate(False)
        self.body2.pack()

        # Sex
        self.sex_frame = tk.Frame(self.body2, width=350, height=40, bg=app.getColor(2))
        self.sex_frame.pack_propagate(False)
        self.sex_frame.pack(pady=(40, 0))

        self.sex_label = tk.Label(self.sex_frame, text="Sex", font=("Helvetica", 10), bg=app.getColor(2))
        self.sex_label.pack(side="left", padx=50)
        self.sex_value_var = tk.StringVar(value="")
        self.sex_value = tk.Label(self.sex_frame, textvariable=self.sex_value_var, font=("Helvetica", 10), bg=app.getColor(2))
        self.sex_value.pack(side="right", padx=50)

        # Year Level
        self.year_frame = tk.Frame(self.body2, width=350, height=40, bg=app.getColor(2))
        self.year_frame.pack_propagate(False)
        self.year_frame.pack()

        self.year_label = tk.Label(self.year_frame, text="Year Level", bg=app.getColor(2))
        self.year_label.pack(side="left", padx=50)
        self.year_value_var = tk.StringVar(value="")
        self.year_value = tk.Label(self.year_frame, textvariable=self.year_value_var, bg=app.getColor(2))
        self.year_value.pack(side="right", padx=50)

        # Program Code
        self.program_frame = tk.Frame(self.body2, width=350, height=40, bg=app.getColor(2))
        self.program_frame.pack_propagate(False)
        self.program_frame.pack()

        self.program_label = tk.Label(self.program_frame, text="Program Code", bg=app.getColor(2))
        self.program_label.pack(side="left", padx=(50,0))
        self.program_value_var = tk.StringVar(value="")
        self.program_value = tk.Label(self.program_frame, textvariable=self.program_value_var, bg=app.getColor(2))
        self.program_value.pack(side="right", padx=(0,50))

    def update_stud_info_values(self):
        self.full_name_var.set(self.app.getMainStud()[FNAME] + " " + self.app.getMainStud()[LNAME])
        self.id_var.set(str(self.app.getMainStud()[ID])[:4] + "-" + str(self.app.getMainStud()[ID])[4:8])
        self.sex_value_var.set(self.app.getMainStud()[SEX])
        self.year_value_var.set(self.app.getMainStud()[YRLVL] + " Year")
        self.program_value_var.set(self.app.getMainStud()[PCODE] + " ({})".format(self.app.getMainStud()[CCODE]))


    def transition(self):
        self.update_stud_info_values()
        self.frame2.pack()

    def getMainFrame(self):
        return self.frame2
    

class Frame3: # Add Studdent Frame
    def __init__(self, app):
        colorNum = app.getColor(2)
        self.app = app
        self.frame3 = tk.Frame(app.getRoot(), width=682.5, height=590, bg=app.getColor(0))
        self.frame3.pack_propagate(False)

        self.header = tk.Frame(self.frame3, width=682.5, height=50, bg=app.getColor(0))
        self.header.pack_propagate(False)
        self.header.pack()

        style = ttk.Style()
        style.configure('TButton', background=app.getColor(0), foreground=app.getColor(0))
        self.back_button = ttk.Button(self.header, text="Back", width=5, command=lambda: [self.clear_entries, app.transition_frames(app.frame1_obj)], style='TButton')
        self.back_button.pack(side="left", padx=10)

        self.body1 = tk.Frame(self.frame3, width=682.5, height=540, bg=app.getColor(0))
        self.body1.pack_propagate(False)
        self.body1.pack()

        # Image PFP
        self.canvas2 = tk.Canvas(self.body1, width=175, height=175, highlightthickness=0)
        self.canvas2.pack(pady=20)

        image = Image.open("./assets/image.jpg")
        image = image.resize((175, 175))
        photo = ImageTk.PhotoImage(image)

        self.canvas2.create_image(87.5, 87.5, image=photo, anchor=tk.CENTER)
        self.canvas2.image = photo  # Keep a reference to avoid garbage collection

        self.canvas2.create_oval(-50, -50, 225, 225, outline=app.getColor(0), width=100)

        # Frame for Entries
        self.entry_frame_height = 40
        self.entry_frame = tk.Frame(self.body1, width=290, height=200, bg=app.getColor(0))
        self.entry_frame.pack()

        # First Name
        self.first_name_frame = tk.Frame(self.entry_frame, width=290, height=self.entry_frame_height, bg=colorNum)
        self.first_name_frame.pack_propagate(False)
        self.first_name_frame.pack()

        self.first_name_label = tk.Label(self.first_name_frame, text="First Name:", font=("Helvetica", 13), bg=colorNum)
        self.first_name_label.pack(side="left", padx=(20, 0))

        self.first_name_entry = ttk.Entry(self.first_name_frame)
        self.first_name_entry.pack(side="right", padx=(0, 20))

        # Last Name
        self.last_name_frame = tk.Frame(self.entry_frame, width=290, height=self.entry_frame_height, bg=colorNum)
        self.last_name_frame.pack_propagate(False)
        self.last_name_frame.pack()

        self.last_name_label = tk.Label(self.last_name_frame, text="Last Name:", font=("Helvetica", 13), bg=colorNum)
        self.last_name_label.pack(side="left", padx=(20, 0))

        self.last_name_entry = ttk.Entry(self.last_name_frame)
        self.last_name_entry.pack(side="right", padx=(0, 20))

        # ID Number
        self.id_num_frame = tk.Frame(self.entry_frame, width=290, height=self.entry_frame_height, bg=colorNum)
        self.id_num_frame.pack_propagate(False)
        self.id_num_frame.pack()

        self.id_num_label = tk.Label(self.id_num_frame, text="ID Number:", font=("Helvetica", 13), bg=colorNum)
        self.id_num_label.pack(side="left", padx=(20, 0))

        self.id_num_entry = ttk.Entry(self.id_num_frame)
        self.id_num_entry.pack(side="right", padx=(0, 20))

        # Sex
        self.sex_frame = tk.Frame(self.entry_frame, width=290, height=self.entry_frame_height, bg=colorNum)
        self.sex_frame.pack_propagate(False)
        self.sex_frame.pack()

        self.sex_label = tk.Label(self.sex_frame, text="Sex:", font=("Helvetica", 13), bg=colorNum)
        self.sex_label.pack(side="left", padx=(20, 0))

        values = ["Male", "Female"]
        self.sex_cb = ttk.Combobox(self.sex_frame, values=values, state='readonly', width=17)
        self.sex_cb.pack(side="right", padx=(0, 20))

        # Year Level
        self.year_level_frame = tk.Frame(self.entry_frame, width=290, height=self.entry_frame_height, bg=colorNum)
        self.year_level_frame.pack_propagate(False)
        self.year_level_frame.pack()

        self.year_level_label = tk.Label(self.year_level_frame, text="Year Level:", font=("Helvetica", 13), bg=colorNum)
        self.year_level_label.pack(side="left", padx=(20, 0))

        values = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
        self.year_level_cb = ttk.Combobox(self.year_level_frame, values=values, state='readonly', width=17)
        self.year_level_cb.pack(side="right", padx=(0, 20))

        # College Code
        self.college_code_frame = tk.Frame(self.entry_frame, width=290, height=self.entry_frame_height, bg=colorNum)
        self.college_code_frame.pack_propagate(False)
        self.college_code_frame.pack()

        self.college_code_label = tk.Label(self.college_code_frame, text="College:", font=("Helvetica", 13), bg=colorNum)
        self.college_code_label.pack(side="left", padx=(20, 0))

        collegeValues = []
        for i in app.programs_database:
            if i[0] not in collegeValues:
                collegeValues.append(i[0])
        self.college_code_cb = ttk.Combobox(self.college_code_frame, values=collegeValues, state='readonly', width=17)
        self.college_code_cb.pack(side="right", padx=(0, 20))



        # Program Code
        self.program_code_frame = tk.Frame(self.entry_frame, width=290, height=self.entry_frame_height, bg=colorNum)
        self.program_code_frame.pack_propagate(False)
        self.program_code_frame.pack()

        self.program_code_label = tk.Label(self.program_code_frame, text="Program:", font=("Helvetica", 13), bg=colorNum)
        self.program_code_label.pack(side="left", padx=(20, 0))

        programValues = []
        self.program_code_cb = ttk.Combobox(self.program_code_frame, values=programValues, state='readonly', width=17)
        self.program_code_cb.pack(side="right", padx=(0, 20))   

        self.college_code_cb.bind("<<ComboboxSelected>>", self.update_program_values)


        # Submit
        self.entries = None
        self.submit_button = ttk.Button(self.body1, text="Submit", command=self.submit_func)
        self.submit_button.pack(pady=(10, 0))
    
    def update_program_values(self, event):
        self.program_code_cb.set('')
        college = self.college_code_cb.get()
        programValues = []
        for i in self.app.programs_database:
            if (college == i[0]):
                programValues.append(i[1])
        self.program_code_cb['values'] = programValues

    def submit_func(self):
        self.entries = [self.first_name_entry, self.last_name_entry, self.sex_cb, self.id_num_entry, 
                   self.year_level_cb, self.college_code_cb, self.program_code_cb]
        values = []
        for e in self.entries:
            if not e.get():
                self.alert_message("Input Error", "All fields must be filled out.")
                return
            values.append(e.get())
        values[FNAME] = values[FNAME].capitalize()
        values[LNAME] = values[LNAME].capitalize()
        # Name Error
        for c in values[FNAME].replace(" ", ""):
            if not c.isalpha():
                self.alert_message("Input Error", "First Name must not contain digits or any symbols.")
                return
        for c in values[LNAME].replace(" ", ""):
            if not c.isalpha():
                self.alert_message("Input Error", "Last Name must not contain digits or any symbols.")
                return

        # ID Number error
        if "-" in values[ID]:
            values[ID] = values[ID].replace("-", "")

        for c in values[ID]:
            if c.isalpha():
                self.alert_message("Input Error", "ID Number must only contain digits or '-'.")
                return
        
        if len(values[ID]) != 8:
            self.alert_message("Input Error", "ID Numbers must be 8 digits.")
            return

        if self.app.get_student(values[ID]) != None:
            self.alert_message("Input Error", "Student with {} ID already exists.".format(values[3]))
            return
        
        values[YRLVL] = values[YRLVL][:3]
        self.add_student(values)
        self.clear_entries()
        self.app.setMainStud(None)

    def alert_message(self, title, text):
        tk.messagebox.showerror(title, text)

    def add_student(self, values):
        self.app.add_student(values)
    def clear_entries(self):
        for e in self.entries:
            if isinstance(e, ttk.Entry):
                e.delete(0, tk.END)

        self.sex_cb.set('')
        self.year_level_cb.set('')
        self.program_code_cb.set('')
        self.college_code_cb.set('')
        self.app.transition_frames(self.app.frame1_obj)

    def transition(self):
        collegeValues = []
        for i in self.app.programs_database:
            if i[0] not in collegeValues:
                collegeValues.append(i[0])
        self.college_code_cb['values'] = collegeValues
        self.frame3.pack()

class Frame4: # SETTINGS FRAME
    def __init__(self, app):
        self.app = app
        self.searchValues = {"First Name" : 0, "Last Name" : 1, "ID#" : 3, "Year Level" : 4}
        self.searchValuesProgram = {"College Code" : 0, "Program Code" : 1}
        self.searchValuesCollege = {"College Name" : 0, "College Code" : 1}
        self.filterValues = [{"None" : None, "Sex" : 2, "Year Level" : 4, "College Code" : 5, "Program Code" : 6}, 
                             {"None" : None, "College Code" : 0, "Program Code" : 1},
                             {"None" : None, "College Code" : 1}]
        self.create_widgets(app)

    def create_widgets(self, app):
        self.frame4 = tk.Frame(app.getRoot(), bg=app.getColor(0))
        self.frame4.pack()

        # List
        self.list_frame = tk.Frame(self.frame4, width=150, height=20)
        self.list_frame.pack_propagate(False)
        self.list_frame.pack(pady=(10, 0))

        self.list_label = tk.Label(self.list_frame, text="List Mode: ")
        self.list_label.pack(side="left")

        self.list_cb = ttk.Combobox(self.list_frame, state='readonly', values=["Students", "Programs", "Colleges"], width=8)
        self.list_cb.pack(side="right")
        self.list_cb.bind("<<ComboboxSelected>>", self.cboxEvent)

        # Search By
        self.search_frame = tk.Frame(self.frame4, width=150, height=20)
        self.search_frame.pack_propagate(False)
        self.search_frame.pack(pady=(10,0))

        self.search_label = tk.Label(self.search_frame, text="Search By: ")
        self.search_label.pack(side="left")


        self.search_cb = ttk.Combobox(self.search_frame, state='readonly', values=list(self.searchValues.keys()), width=8)
        self.search_cb.pack(side="right")

        # Sort By
        self.sort_frame = tk.Frame(self.frame4, width=150, height=20)
        self.sort_frame.pack_propagate(False)
        self.sort_frame.pack(pady=(10,0))

        self.sort_label = tk.Label(self.sort_frame, text="Order: ")
        self.sort_label.pack(side="left")

        self.sortValues = {"Ascending" : True, "Descending" : False}
        self.sort_cb = ttk.Combobox(self.sort_frame, state='readonly', values=list(self.sortValues.keys()), width=8)
        self.sort_cb.pack(side="right")

        # Filter
        self.filter_frame = tk.Frame(self.frame4, width=150, height=20)
        self.filter_frame.pack_propagate(False)
        self.filter_frame.pack(pady=(10,0))

        self.filter_label = tk.Label(self.filter_frame, text="Filter: ")
        self.filter_label.pack(side="left")

        self.filter_cb = ttk.Combobox(self.filter_frame, state='readonly', values=[], width=8)
        self.filter_cb.pack(side="right")

        # Filter Entry
        self.filter_entry_frame = tk.Frame(self.frame4, width=150, height=20)
        self.filter_entry_frame.pack_propagate(False)
        self.filter_entry_frame.pack()


        self.filter_entry = ttk.Entry(self.filter_entry_frame, width=11)
        self.filter_entry.pack(side="right")

        # Done
        self.done_button = ttk.Button(self.frame4, text="DONE", command=self.done_button)
        self.done_button.pack(pady=10)

    def cboxEvent(self, event):
        if self.list_cb.get() == "Students":
            self.search_cb['values'] = list(self.searchValues.keys())
            self.filter_cb.set("None")
            self.filter_cb['values'] = list(self.filterValues[0].keys())
        elif self.list_cb.get() == "Programs":
            self.search_cb['values'] = list(self.searchValuesProgram.keys())
            self.filter_cb.set("None")
            self.filter_cb['values'] = list(self.filterValues[1].keys())
        elif self.list_cb.get() == "Colleges":
            self.search_cb['values'] = list(self.searchValuesCollege.keys())
            self.filter_cb.set("None")
            self.filter_cb['values'] = list(self.filterValues[2].keys())

    def done_button(self):
        if not self.list_cb.get():
            messagebox.showerror("Input Error", "Please select a list mode.")
            return
        elif not self.search_cb.get():
            messagebox.showerror("Input Error", "Please select a search type.")
            return
        elif not self.sort_cb.get():
            messagebox.showerror("Input Error", "Please select a sort type.")
            return
        self.app.filter_value = self.filter_entry.get()

        if self.list_cb.get() == "Students":
            self.app.setSearchSet(self.searchValues[self.search_cb.get()])
            self.app.sort_students(self.searchValues[self.search_cb.get()], self.sortValues[self.sort_cb.get()])
            self.app.list_mode = 0
            self.app.filter_mode = self.filterValues[0][self.filter_cb.get()]
            self.app.transition_frames(self.app.frame1_obj)
        elif self.list_cb.get() == "Programs":
            self.app.setSearchSet(self.searchValuesProgram[self.search_cb.get()])
            self.app.sort_programs(self.searchValuesProgram[self.search_cb.get()], self.sortValues[self.sort_cb.get()])
            self.app.list_mode = 1
            self.app.filter_mode = self.filterValues[1][self.filter_cb.get()]
            self.app.transition_frames(self.app.frame1_obj)
        elif self.list_cb.get() == "Colleges":
            self.app.setSearchSet(self.searchValuesCollege[self.search_cb.get()])
            self.app.sort_colleges(self.searchValuesCollege[self.search_cb.get()], self.sortValues[self.sort_cb.get()])
            self.app.list_mode = 2
            self.app.filter_mode = self.filterValues[2][self.filter_cb.get()]
            self.app.transition_frames(self.app.frame8_obj)


        

    def updateValues(self):
        # if self.app.list_mode == 0:
        #     self.search_cb['values'] = list(self.searchValues.keys())
        #     self.sort_cb['values'] = list(self.sortValues.keys())
        # elif self.app.list_mode == 1:
        #     self.search_cb['values'] = ["College Code", "Program Code"]
        #     self.sort_cb['values'] = ["Ascending", "Descending"]
        # elif self.app.list_mode == 2:
        #     self.search_cb['values'] = ["College Name", "College Code"]
        #     self.sort_cb['values'] = ["Ascending", "Descending"]

        self.search_cb['values'] = []
        self.filter_cb['values'] = []

    def transition(self):
        self.list_cb.set('')
        self.search_cb.set('')
        self.sort_cb.set('')
        self.filter_cb.set('')
        self.updateValues()
        self.app.filter_mode = None
        self.app.filter_value = None
        self.frame4.pack()

class Frame5: # ADD PROGRAM FRAME
    def __init__(self, app):
        self.app = app
        self.create_widgets(app)


    def create_widgets(self, app):
        self.frame5 = tk.Frame(app.getRoot(), bg=app.getColor(0))
        self.frame5.pack()
        # Add College Frame
        self.AC_frame = tk.Frame(self.frame5, width=300, height=200, bg=app.getColor(1))
        self.AC_frame.pack(pady=(20, 0), side='top')

        AC_frames = []
        for i in range(0, 3):
            AC_frames.append(tk.Frame(self.AC_frame, width=270, height=30, bg="white"))
            AC_frames[i].pack_propagate(False)
            AC_frames[i].pack(side='top', pady=(10, 0))

        self.college_code_label = tk.Label(AC_frames[0], text="College Code", font=('helvetica', 15))
        self.college_code_label.pack(side='left', padx=(0, 20))
        self.college_code_cb = ttk.Combobox(AC_frames[0], width=10, font=('helvetica', 15), values=app.getProgramsList(), state='readonly')
        self.college_code_cb.pack(side='right')

        self.program_code_label = tk.Label(AC_frames[1], text="Program Code", font=('helvetica', 15))
        self.program_code_label.pack(side='left')
        self.program_code_entry = ttk.Entry(AC_frames[1], width=10, font=('helvetica', 15))
        self.program_code_entry.pack(side='right')

        self.program_name_label = tk.Label(AC_frames[2], text="Program Name", font=('helvetica', 15))
        self.program_name_label.pack(side='left')
        self.program_name_entry = ttk.Entry(AC_frames[2], width=10, font=('helvetica', 15))
        self.program_name_entry.pack(side='right')

        self.add_button = ttk.Button(self.AC_frame,  text="ADD", command=self.add_button_func)
        self.add_button.pack(side='top', pady=(10, 0))

        # Remove PrograM Frame
        self.RC_Frame = tk.Frame(self.frame5, width=200, height=200, bg=app.getColor(1))
        self.RC_Frame.pack(pady=(30,0))

        RC_Frames = []
        for i in range(0, 2):
            RC_Frames.append(tk.Frame(self.RC_Frame, width=270, height=30, bg="white"))
            RC_Frames[i].pack_propagate(False)
            RC_Frames[i].pack(pady=(10,0))

        self.rcollege_label = tk.Label(RC_Frames[0], text="College Code", font=('helvetica', 15))
        self.rcollege_label.pack(side='left')
        self.rcollege_cb = ttk.Combobox(RC_Frames[0], width=10, font=('helvetica', 15), values=app.getProgramsList(), state='readonly')
        self.rcollege_cb.pack(side='right')
        self.rcollege_cb.bind('<<ComboboxSelected>>', self.upd_rprogram_code_cb)

        self.rprogram_code_label = tk.Label(RC_Frames[1], text="Program Code", font=('helvetica', 15))
        self.rprogram_code_label.pack(side='left')
        self.rprogram_code_cb = ttk.Combobox(RC_Frames[1], width=10, font=('helvetica', 15), state='readonly')
        self.rprogram_code_cb.pack(side='right')

        self.remove_button = ttk.Button(self.RC_Frame, text="Remove", command=self.remove_button_func)
        self.remove_button.pack(pady=(10, 0))

        self.exit_button = ttk.Button(self.frame5, text="Exit", command=self.exit_button_func)
        self.exit_button.pack(side='top', pady=(10, 0))

    def upd_rprogram_code_cb(self, e):
        v = []
        self.app.updatePrograms_database()
        for i in self.app.getProgramDb():
            if self.rcollege_cb.get() == i[0]:
                v.append(i[1])
        self.rprogram_code_cb.config(values=v)

    def add_button_func(self):
        self.app.add_program([self.college_code_cb.get(), self.program_code_entry.get(), self.program_name_entry.get()])
        self.exit_button_func()
        
        self.college_code_cb.delete(0, tk.END)
        self.program_code_entry.delete(0, tk.END)
        self.program_name_entry.delete(0, tk.END)

        self.rcollege_cb.config(values=self.app.getProgramsList())
        self.rprogram_code_cb.config(values=[])

    def remove_button_func(self):
        self.app.delete_program(self.rprogram_code_cb.get())
        self.exit_button_func()

        self.rcollege_cb.set('')
        self.rprogram_code_cb.set('')

        self.rcollege_cb.config(values=self.app.getProgramsList())
        self.rprogram_code_cb.config(values=[])

    def exit_button_func(self):
        self.app.transition_frames(self.app.frame1_obj)

    def transition(self):
        v = []
        self.app.updateColleges_database()
        for i in self.app.colleges_database:
            if i[1] not in self.app.colleges_database:
                v.append(i[1])
        self.college_code_cb.config(values=v)

        self.rcollege_cb.config(values=self.app.getProgramsList())

        self.frame5.pack()

class Frame6(Frame3): # EDIT STUDENT FRAME
    def add_student(self, values):
        self.app.replace_student(self.app.getMainStud()[ID], values)

    def submit_func(self):
        self.entries = [self.first_name_entry, self.last_name_entry, self.sex_cb, self.id_num_entry, 
                   self.year_level_cb, self.college_code_cb, self.program_code_cb]
        values = []
        for e in self.entries:
            if not e.get():
                self.alert_message("Input Error", "All fields must be filled out.")
                return
            values.append(e.get())
        values[FNAME] = values[FNAME].capitalize()
        values[LNAME] = values[LNAME].capitalize()
        # Name Error
        for c in values[FNAME].replace(" ", ""):
            if not c.isalpha():
                self.alert_message("Input Error", "First Name must not contain digits or any symbols.")
                return
        for c in values[LNAME].replace(" ", ""):
            if not c.isalpha():
                self.alert_message("Input Error", "Last Name must not contain digits or any symbols.")
                return

        # ID Number error
        if "-" in values[ID]:
            values[ID] = values[ID].replace("-", "")

        for c in values[ID]:
            if c.isalpha():
                self.alert_message("Input Error", "ID Number must only contain digits or '-'.")
                return
        
        if len(values[ID]) != 8:
            self.alert_message("Input Error", "ID Numbers must be 8 digits.")
            return

        
        values[YRLVL] = values[YRLVL][:3]
        self.add_student(values)
        self.clear_entries()
        self.app.setMainStud(None)

    def transition(self):
        super().transition()
        self.app.modify_mode = False
        if self.app.getMainStud() is not None:

            self.first_name_entry.delete(0, tk.END)
            self.first_name_entry.insert(0, self.app.getMainStud()[FNAME])
            self.last_name_entry.delete(0, tk.END)
            self.last_name_entry.insert(0, self.app.getMainStud()[LNAME])
            if self.app.getMainStud() is not None:
                self.id_num_entry.delete(0, tk.END)
                self.id_num_entry.insert(0, str(self.app.getMainStud()[ID])[:4] + "-" + str(self.app.getMainStud()[ID])[4:8])
                self.sex_cb.set(self.app.getMainStud()[SEX])
            self.year_level_cb.set(self.app.getMainStud()[YRLVL] + " Year")
            self.college_code_cb.set(self.app.getMainStud()[CCODE])
            self.update_program_values(None)
            self.program_code_cb.set(self.app.getMainStud()[PCODE])

class Frame7(Frame5): # ADD COLLEGE FRAME
    def create_widgets(self, app):
        self.frame5 = tk.Frame(app.getRoot(), bg=app.getColor(0))
        self.frame5.pack()
        # Add College Frame
        self.AC_frame = tk.Frame(self.frame5, width=300, height=200, bg=app.getColor(1))
        self.AC_frame.pack(pady=(20, 0), side='top')

        AC_frames = []
        for i in range(0, 2):
            AC_frames.append(tk.Frame(self.AC_frame, width=270, height=30, bg="white"))
            AC_frames[i].pack_propagate(False)
            AC_frames[i].pack(side='top', pady=(10, 0))

        self.college_code_label = tk.Label(AC_frames[0], text="College Code", font=('helvetica', 15))
        self.college_code_label.pack(side='left', padx=(0, 20))
        self.college_code_entry = ttk.Entry(AC_frames[0], width=10, font=('helvetica', 15))
        self.college_code_entry.pack(side='right')

        self.college_name_label = tk.Label(AC_frames[1], text="Program Code", font=('helvetica', 15))
        self.college_name_label.pack(side='left')
        self.college_name_entry = ttk.Entry(AC_frames[1], width=10, font=('helvetica', 15))
        self.college_name_entry.pack(side='right')

        self.add_button = ttk.Button(self.AC_frame,  text="ADD", command=self.add_button_func)
        self.add_button.pack(side='top', pady=(10, 0))

        # Remove College Frame
        self.RC_Frame = tk.Frame(self.frame5, width=200, height=200, bg=app.getColor(1))
        self.RC_Frame.pack(pady=(30,0))

        RC_Frames = []
        for i in range(0, 1):
            RC_Frames.append(tk.Frame(self.RC_Frame, width=270, height=30, bg="white"))
            RC_Frames[i].pack_propagate(False)
            RC_Frames[i].pack(pady=(10,0))

        self.rcollege_code_label = tk.Label(RC_Frames[0], text="College", font=('helvetica', 15))
        self.rcollege_code_label.pack(side='left')
        self.rcollege_code_cb = ttk.Combobox(RC_Frames[0], width=10, font=('helvetica', 15), values=self.app.colleges_list, state='readonly')
        self.rcollege_code_cb.pack(side='right')
        self.remove_button = ttk.Button(self.RC_Frame, text="Remove", command=self.remove_button_func)
        self.remove_button.pack(pady=(10, 0))

        self.exit_button = ttk.Button(self.frame5, text="Exit", command=self.exit_button_func)
        self.exit_button.pack(side='top', pady=(10, 0))

    def upd_rprogram_code_cb(self, e):
        pass

    def add_button_func(self):
        self.app.add_college([self.college_name_entry.get(), self.college_code_entry.get()])
        self.exit_button_func()
        
        self.college_code_entry.delete(0, tk.END)
        self.college_name_entry.delete(0, tk.END)

        self.rcollege_code_cb.config(values=[])

    def remove_button_func(self):
        self.app.delete_college(self.rcollege_code_cb.get())
        self.exit_button_func()

        self.rcollege_code_cb.set('')
        self.rcollege_code_cb.config(values=[])

    def exit_button_func(self):
        self.app.transition_frames(self.app.frame8_obj)

    def transition(self):
        self.rcollege_code_cb.config(values=[college[1] for college in self.app.colleges_database]) # Update cbbox values
        self.frame5.pack()

class Frame8(Frame1): # CRUDL COLLEGES
    def __init__(self, app):
        self.app = app
        self.entry_str_var = tk.StringVar()
        self.entry_str_var.trace_add(mode="write", callback=self.on_entry_updated)
        self.acquired_list = app.colleges_database
        self.page = 1
        self.maxPage = ceil(len(self.acquired_list)/12)
        self.create_widgets(app)

    def show_list(self):
        if self.app.filter_mode is not None:
            self.filter_list()
        self.add_student_button.configure(command=lambda: self.app.transition_frames(self.app.frame7_obj))
        self.maxPage = ceil(len(self.acquired_list)/12)
        self.page_label2_var.set(f"of {self.maxPage}")
        for widget in self.bot_frame.winfo_children():
            widget.pack_forget()
        for i in range((self.page - 1) * 12, self.page * 12):
            if i < len(self.acquired_list):
                MiniProfile(self.app, self.bot_frame, self.acquired_list[i])

    def label_frame_upd(self, int_label):

        labels = {"College Name":235, "College Code":210}
        for i in self.labels_frame.winfo_children():
            i.pack_forget()
        for i in list(labels.keys()):
            self.label_ = tk.Label(master=self.labels_frame, bg=self.app.getColor(2), text=i)
            self.label_.pack(side="left", padx=(labels[i],0))


    def transition(self):
        self.acquired_list = self.app.colleges_database
        self.frame1.pack()
        self.show_list()

class FrameEditProgram:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.getRoot(), bg=app.getColor(0))
        self.frame.pack()

        # Create input fields
        self.program_code_var = tk.StringVar()
        self.program_name_var = tk.StringVar()

        self.program_code_frame = tk.Frame(self.frame, bg=app.getColor(0))
        self.program_code_frame.pack(pady=(20, 0))
        self.program_code_label = tk.Label(self.frame, text="Program Code:", bg=app.getColor(0))
        self.program_code_label.pack(pady=(10, 0))
        self.program_code_entry = ttk.Entry(self.frame, textvariable=self.program_code_var)
        self.program_code_entry.pack(pady=(0, 10))

        self.program_name_label = tk.Label(self.frame, text="Program Name:", bg=app.getColor(0))
        self.program_name_label.pack(pady=(10, 0))
        self.program_name_entry = ttk.Entry(self.frame, textvariable=self.program_name_var)
        self.program_name_entry.pack(pady=(0, 10))

        # Done button
        self.done_button = ttk.Button(self.frame, text="Done", command=self.done_button_func)
        self.done_button.pack(pady=(20, 0))

        # Exit button
        self.exit_button = ttk.Button(self.frame, text="Exit", command=lambda: self.app.transition_frames(self.app.frame1_obj))
        self.exit_button.pack(pady=(10, 0))

    def transition(self):
        main_program = self.app.main_program
        if main_program:
            self.program_code_var.set(main_program[1])
            self.program_name_var.set(main_program[2])
        self.frame.pack()

    def done_button_func(self):
        program_code = self.program_code_var.get()
        program_name = self.program_name_var.get()

        if not program_code or not program_name:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        self.app.update_program(self.app.main_program[1], [self.app.main_program[0], program_code, program_name])
        self.app.transition_frames(self.app.frame1_obj)

    def getMainFrame(self):
        return self.frame

class FrameEditCollege:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.getRoot(), bg=app.getColor(0), width=300, height=200)
        self.frame.pack()

        # Create input fields
        self.college_code_var = tk.StringVar()
        self.college_name_var = tk.StringVar()

        self.college_code_label = tk.Label(self.frame, text="College Code:", bg=app.getColor(0))
        self.college_code_label.pack(pady=(10, 0))
        self.college_code_entry = ttk.Entry(self.frame, textvariable=self.college_code_var)
        self.college_code_entry.pack(pady=(0, 10))

        self.college_name_label = tk.Label(self.frame, text="College Name:", bg=app.getColor(0))
        self.college_name_label.pack(pady=(10, 0))
        self.college_name_entry = ttk.Entry(self.frame, textvariable=self.college_name_var)
        self.college_name_entry.pack(pady=(0, 10))

        # Done button
        self.done_button = ttk.Button(self.frame, text="Done", command=self.done_button_func)
        self.done_button.pack(pady=(20, 0))

        # Exit button
        self.exit_button = ttk.Button(self.frame, text="Exit", command=lambda: self.app.transition_frames(self.app.frame8_obj))
        self.exit_button.pack(pady=(10, 0))

    def transition(self):
        main_college = self.app.main_college
        if main_college:
            self.college_code_var.set(main_college[1])
            self.college_name_var.set(main_college[0])
        self.frame.pack()

    def done_button_func(self):
        college_code = self.college_code_var.get()
        college_name = self.college_name_var.get()

        if not college_code or not college_name:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        self.app.update_college(self.app.main_college[1], [college_name, college_code])
        self.app.transition_frames(self.app.frame8_obj)

    def getMainFrame(self):
        return self.frame