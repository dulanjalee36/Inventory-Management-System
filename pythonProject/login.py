import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

# ================= DATABASE CONNECTION =================
def connect_database():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="inventory_system"
        )
        return connection
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None

# ================= CREATE USERS TABLE IF NOT EXISTS =================
def create_users_table():
    connection = connect_database()
    if connection is None:
        return
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """)
    connection.commit()
    connection.close()

# Call table creation at start
create_users_table()

# ================= REGISTER FUNCTION =================
def register():
    username = user_entry.get()
    password = pass_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All Fields Are Required")
        return

    connection = connect_database()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)",
                       (username, password))
        connection.commit()
        messagebox.showinfo("Success", "Registration Successful!")
        user_entry.delete(0, tk.END)
        pass_entry.delete(0, tk.END)
    except pymysql.err.IntegrityError:
        messagebox.showerror("Error", "Username Already Exists!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        connection.close()


# ================= LOGIN FUNCTION =================
def login():
    username = user_entry.get()
    password = pass_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All Fields Are Required")
        return

    connection = connect_database()
    if connection is None:
        return

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                   (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login Successful!")
        root.destroy()
        import main
        main.open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

    connection.close()


# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Inventory Login")
root.geometry("1350x710+0+0")
root.resizable(False, False)
root.config(bg="#f0f2f5")

# ================= HEADER =================
header_frame = tk.Frame(root, bg="#010c48", height=100)
header_frame.pack(fill="x")

try:
    logo_img = Image.open("inventory.png").resize((80, 80))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header_frame, image=logo_photo, bg="#010c48")
    logo_label.pack(side="left", padx=20, pady=10)
except:
    pass

title_label = tk.Label(header_frame,
                       text="Inventory Management System",
                       font=("Arial", 32, "bold"),
                       bg="#010c48", fg="white")
title_label.pack(side="left", padx=10)

# ================= BODY =================
split_frame = tk.Frame(root, bg="#f0f2f5")
split_frame.pack(fill="both", expand=True)

left_frame = tk.Frame(split_frame, bg="#f0f2f5")
left_frame.pack(side="left", fill="both", expand=True)

try:
    left_img = Image.open("first.png").resize((600, 600))
    left_photo = ImageTk.PhotoImage(left_img)
    left_label = tk.Label(left_frame, image=left_photo, bg="#f0f2f5")
    left_label.pack(expand=True)
except:
    pass

right_frame = tk.Frame(split_frame, bg="white", bd=2, relief="ridge")
right_frame.pack(side="left", fill="both", expand=True, padx=50, pady=50)

try:
    avatar_img = Image.open("man (1).png").resize((120, 120))
    avatar_photo = ImageTk.PhotoImage(avatar_img)
    avatar_label = tk.Label(right_frame, image=avatar_photo, bg="white")
    avatar_label.pack(pady=20)
except:
    pass

login_title = tk.Label(right_frame,
                       text="LOGIN / REGISTER",
                       font=("Arial", 20, "bold"),
                       bg="white")
login_title.pack(pady=10)

# Username
tk.Label(right_frame, text="Username",
         font=("Arial", 12), bg="white").pack(pady=5)
user_entry = tk.Entry(right_frame,
                      font=("Arial", 12),
                      width=25, bd=2, relief="groove")
user_entry.pack(pady=5)

# Password
tk.Label(right_frame, text="Password",
         font=("Arial", 12), bg="white").pack(pady=5)
pass_entry = tk.Entry(right_frame,
                      font=("Arial", 12),
                      show="*", width=25,
                      bd=2, relief="groove")
pass_entry.pack(pady=5)

# Buttons Frame
btn_frame = tk.Frame(right_frame, bg="white")
btn_frame.pack(pady=20)

login_btn = tk.Button(btn_frame,
                      text="Login",
                      font=("Arial", 12, "bold"),
                      bg="#010c48",
                      fg="white",
                      width=12,
                      command=login)
login_btn.grid(row=0, column=0, padx=10)

register_btn = tk.Button(btn_frame,
                         text="Register",
                         font=("Arial", 12, "bold"),
                         bg="green",
                         fg="white",
                         width=12,
                         command=register)
register_btn.grid(row=0, column=1, padx=10)

# ================= FOOTER =================
footer = tk.Label(root,
                  text="© 2026 Inventory System. All rights reserved.",
                  bg="#f0f2f5",
                  fg="gray",
                  font=("Arial", 10))
footer.pack(side="bottom", pady=10)

root.mainloop()