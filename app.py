import customtkinter
import os
from tkinter import*
from tkinter import filedialog as fd
import tkinter.messagebox
from tkinter.messagebox import showinfo
from database_manager import DatabaseManager
from hash import hasher
import atexit

hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = 'admin'
port_id = 5432

db = DatabaseManager(hostname, username, pwd, database, port_id)

def view_data():
    
    files = db.view_db()

    
    db_window = customtkinter.CTkToplevel(app)
    db_window.title("Files Hashed")
    db_window.geometry("700x700")

    db_window.transient(app)
    db_window.grab_set()
    db_window.focus_force()

    
    scrollable_frame = customtkinter.CTkScrollableFrame(db_window, width=380, height=350)
    scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

    
    if files:
        for file, timestamp in files:
            label = customtkinter.CTkLabel(scrollable_frame, text=f"{file} (Last Modified: {timestamp})")
            label.pack(pady=5)

    else:
        label = customtkinter.CTkLabel(scrollable_frame, text="No files found.")
        label.pack(pady=20)


def hash_files():
    filetypes = ( 
        ('text files', '*.txt'),
        ('docx files','*.docx')
    )

    filenames = fd.askopenfilenames(
        title='Select files',
        initialdir='/',
        filetypes=filetypes
    )

    showinfo(
        title='Selected Files',   
        message=filenames 
    )

    for file in filenames:
        file_hasher = hasher(file)
        file_hash = file_hasher.hash_file()
        db.add_to_db(file, file_hash)  


USERNAME = "123"
PASSWORD = "123"

def login_prompt():
    login_win = customtkinter.CTkToplevel(app)
    login_win.title("Login")
    login_win.geometry("300x200")

    login_win.transient(app)
    login_win.grab_set()
    login_win.focus_force()

    customtkinter.CTkLabel(login_win, text="Username").pack(pady=5)
    username_entry = customtkinter.CTkEntry(login_win)
    username_entry.pack(pady=5)

    customtkinter.CTkLabel(login_win, text="Password").pack(pady=5)
    password_entry = customtkinter.CTkEntry(login_win, show="*")
    password_entry.pack(pady=5)

    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()

        if username == USERNAME and password == PASSWORD:
            login_win.destroy()
            hash_files()  # Call main hashing function
        else:
            tkinter.messagebox.showerror("Login Failed", "Invalid credentials.")

    customtkinter.CTkButton(login_win, text="Login", command=check_credentials).pack(pady=10)



def check_integrity():
    result_window = customtkinter.CTkToplevel(app)
    result_window.title("Integrity Check Results")
    result_window.geometry("500x400")

    result_window.transient(app)     
    result_window.grab_set()         
    result_window.focus_force() 

    scroll = customtkinter.CTkScrollableFrame(result_window, width=480, height=360)
    scroll.pack(padx=10, pady=10, fill="both", expand=True)

    files = db.fetch_all_hashes()

    if not files:
        customtkinter.CTkLabel(scroll, text="No records in database.").pack(pady=10)
        return

    for filename, stored_hash in files:
        if not os.path.exists(filename):
            label = customtkinter.CTkLabel(scroll, text=f"{filename} - ⚠️ File Missing")
            label.pack(pady=5)
            continue

        current_hash = hasher(filename).hash_file()
        if current_hash == stored_hash:
            label = customtkinter.CTkLabel(scroll, text=f"{filename} - ✅ Unchanged")
        else:
            label = customtkinter.CTkLabel(scroll, text=f"{filename} - ❌ Modified")
        label.pack(pady=5)

def remove_file():
    def check_admin_and_proceed():
        username = username_entry.get()
        password = password_entry.get()

        if username == USERNAME and password == PASSWORD:
            login_win.destroy()
            proceed_with_removal()
        else:
            tkinter.messagebox.showerror("Login Failed", "Invalid credentials.")

    def proceed_with_removal():
        filetypes = (
            ('text files', '*.txt'),
            ('docx files', '*.docx'),
        )

        filenames = fd.askopenfilenames(
            title='Select file(s) to remove from database',
            initialdir='/',
            filetypes=filetypes
        )

        for file in filenames:
            db.remove_from_db(file)
            tkinter.messagebox.showinfo("Removed", f"{file} removed from database.")

    login_win = customtkinter.CTkToplevel(app)
    login_win.title("Admin Login")
    login_win.geometry("300x200")

    login_win.transient(app)
    login_win.grab_set()
    login_win.focus_force()

    customtkinter.CTkLabel(login_win, text="Username").pack(pady=5)
    username_entry = customtkinter.CTkEntry(login_win)
    username_entry.pack(pady=5)

    customtkinter.CTkLabel(login_win, text="Password").pack(pady=5)
    password_entry = customtkinter.CTkEntry(login_win, show="*")
    password_entry.pack(pady=5)

    customtkinter.CTkButton(login_win, text="Login", command=check_admin_and_proceed).pack(pady=10)

       



app = customtkinter.CTk()
app.title("File Integrity Monitor")
app.geometry("500x500")

button_1 = customtkinter.CTkButton(app, text="Create / Update Database", command=login_prompt)
button_1.pack(pady=40)

button_2 = customtkinter.CTkButton(app, text="Check File Integrity", command=check_integrity)
button_2.pack(pady=40)


button_4 = customtkinter.CTkButton(app, text='View Database', command=view_data)
button_4.pack(pady=40)

button_5 = customtkinter.CTkButton(app, text='Remove File from DB', command=remove_file)
button_5.pack(pady=40)



atexit.register(db.close)
app.mainloop()