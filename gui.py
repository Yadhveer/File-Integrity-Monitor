import hashlib
import mysql
import mysql.connector as mc
import os
from tkinter import*
from tkinter import filedialog as fd
import tkinter.messagebox
from tkinter.messagebox import showinfo
import customtkinter

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  

app = customtkinter.CTk()
app.geometry("500x550")
app.title("File Integrity Monitor")

def run():
    connection = mc.connect(host = "localhost", user = "root", passwd = "toor", database = "fim")
    cursor = connection.cursor()
    cursor.execute("USE fim;")

    cursor.execute(" SELECT File FROM hash; ")
    files = cursor.fetchall()

    while True :
       
                for i in range(0, len(files)):
                    a = files[i]
                    x = a[0]

                    file_object = open(x,"r")

                    text = file_object.read()
                    file_object.close()
                    encoded_text = text.encode()
                    hash = hashlib.sha256(encoded_text)
                    readable_hash = hash.hexdigest()

                    query = """ SELECT Hash FROM hash WHERE File = %s """
                    b = (x,)
                    cursor.execute(query,a)
                    files_check = cursor.fetchall()
                    
                    t = files_check[0]
                    s = t[0]

                    if(s == readable_hash):
                        continue
                    else:
                        print(x)
                        break    
                break

    connection.commit()    
    connection.close()

def specific_file():
    filetypes = ( 
        ('text files', '*.txt'),
        ('docx files','*.docx')
    )

    filenames = fd.askopenfilenames(
        title = 'Select files',
        initialdir = '/',
        filetypes = filetypes
    )

    showinfo(
        title = 'Selected Files',   
        message = filenames 
    )

    connection = mc.connect(host = "localhost", user = "root", passwd = "toor", database = "fim")
    cursor = connection.cursor()
    cursor.execute("USE fim;")

    changed_files = [None] * len(filenames)
    c_index = 0
    unchanged_files = [None] * len(filenames)
    u_index = 0

    for i in range(0, len(filenames)):


        file_object = open(filenames[i],"r")

        text = file_object.read()
        file_object.close()
        encoded_text = text.encode()
        hash = hashlib.sha256(encoded_text)
        readable_hash = hash.hexdigest()

        query = """ SELECT Hash FROM hash WHERE File = %s """
        a = (filenames[i],)
        cursor.execute(query,a)
        files = cursor.fetchall()

        x = files[0]
        b = x[0]

        if b == readable_hash :
            unchanged_files[u_index] = filenames[i]
            u_index += 1

        else :
            changed_files[c_index] = filenames[i]
            c_index += 1     

        for i in range(u_index,len(filenames)):
            unchanged_files[i] = "---"

        for i in range(c_index,len(filenames)):
            changed_files[i] = "---"

        

    change = customtkinter.CTkToplevel(app)
    change.geometry("500x550")
    change.title("File Check")

    combobox1 = customtkinter.CTkOptionMenu(master=change,
                                           values=changed_files)
    combobox1.pack(pady=100)
    combobox1.set("Changed files")

    combobox2 = customtkinter.CTkOptionMenu(master=change,
                                           values=unchanged_files)
    combobox2.pack(pady=100)
    combobox2.set("Unchanged files")

    connection.commit()    
    connection.close() 

def showdb():
    connection = mc.connect(host = "localhost", user = "root", passwd = "toor", database = "fim")
    cursor = connection.cursor()
    cursor.execute("USE fim;")

    cursor.execute("SELECT File FROM hash;")
    files = cursor.fetchall()
    list = [None] * len(files)

    for i in range(0,len(files)):
        a = files[i]
        list[i] =  a[0]

    db = customtkinter.CTkToplevel(app)
    db.geometry("500x550")
    db.title("Database")

    combobox = customtkinter.CTkOptionMenu(master=db,
                                           values=list)
    combobox.pack(pady=100)
    combobox.set("Files in Database")


    connection.commit()    
    connection.close()

def addtodb(file):

    connection = mc.connect(host = "localhost", user = "root", passwd = "toor", database = "fim")
    cursor = connection.cursor()
    cursor.execute("USE fim;")

    for i in range(0, len(file)):


        file_object = open(file[i],"r")

        text = file_object.read()
        file_object.close()
        encoded_text = text.encode()
        hash = hashlib.sha256(encoded_text)
        readable_hash = hash.hexdigest() 

        query = """DELETE FROM hash WHERE File = %s"""
        address = (file[i],)

        cursor.execute(query,address)

        query = """INSERT INTO hash (File,Hash) VALUES (%s, %s) """
        record = (file[i], readable_hash)
        cursor.execute(query,record)
        
    connection.commit()    
    connection.close()
    

def fileselect_createdatabase():
    filetypes = (
        ('text files', '*.txt'),
        ('docx files','*.docx')
    )

    filenames = fd.askopenfilenames(
        title = 'Select files',
        initialdir = '/',
        filetypes = filetypes
    )

    showinfo(
        title = 'Selected Files',   
        message = filenames 
    )

    addtodb(filenames)

def rem_db():
    filetypes = (
        ('text files', '*.txt'),
        ('docx files','*.docx')
    )

    filenames = fd.askopenfilenames(
        title = 'Select files',
        initialdir = '/',
        filetypes = filetypes
    )

    showinfo(
        title = 'Selected Files',   
        message = filenames 
    )

    connection = mc.connect(host = "localhost", user = "root", passwd = "toor", database = "fim")
    cursor = connection.cursor()
    cursor.execute("USE fim;")

    for i in range(0, len(filenames)):

        query = """DELETE FROM hash WHERE File = %s"""
        address = (filenames[i],)
        cursor.execute(query,address)

    connection.commit()    
    connection.close()



button_1 = customtkinter.CTkButton(app, text = 'Create / Update Database', command = fileselect_createdatabase)
button_1.pack(pady = 40)

button_2 = customtkinter.CTkButton(app, text = 'Run File Integrity Check', command = run)
button_2.pack(pady = 40)

button_3 = customtkinter.CTkButton(app, text = 'Check Specific File', command = specific_file)
button_3.pack(pady = 40)

button_4 = customtkinter.CTkButton(app, text = 'View Database', command = showdb)
button_4.pack(pady = 40)

button_5 = customtkinter.CTkButton(app, text = 'Remove from Database', command = rem_db)
button_5.pack(pady = 40)


app.mainloop()