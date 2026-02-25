import tkinter as tk
from tkinter import ttk
import pymysql as db
from tkinter import messagebox


# ================= DATABASE CONNECTION =================
def connect_database():
    try:
        connection = db.connect(
            host='localhost',
            user='root',
            password='12345'
        )
        cursor = connection.cursor()
        return cursor, connection
    except Exception as e:
        messagebox.showerror("Error", f"Database connectivity issue:\n{e}")
        return None, None


def create_database_table():
    cursor, connection = connect_database()
    if not cursor:
        return

    cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
    cursor.execute("USE inventory_system")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_data(
            category_no INT PRIMARY KEY,
            name VARCHAR(100),
            description VARCHAR(200)
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


# ================= FUNCTIONS =================
def treeview_data():
    cursor, connection = connect_database()
    if not cursor:
        return

    cursor.execute("USE inventory_system")
    cursor.execute("SELECT * FROM category_data")
    rows = cursor.fetchall()

    category_tree.delete(*category_tree.get_children())

    for row in rows:
        category_tree.insert('', tk.END, values=row)

    cursor.close()
    connection.close()


def clear_fields():
    category_no_entry.delete(0, tk.END)
    category_name_entry.delete(0, tk.END)
    description_entry.delete("1.0", tk.END)


def select_data(event):
    selected = category_tree.selection()
    if selected:
        values = category_tree.item(selected)['values']

        category_no_entry.delete(0, tk.END)
        category_no_entry.insert(0, values[0])

        category_name_entry.delete(0, tk.END)
        category_name_entry.insert(0, values[1])

        description_entry.delete("1.0", tk.END)
        description_entry.insert("1.0", values[2])


def add_category():
    category_no = category_no_entry.get()
    name = category_name_entry.get()
    description = description_entry.get("1.0", "end-1c")

    if not category_no or not name or not description:
        messagebox.showerror("Error", "All fields are required")
        return

    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT * FROM category_data WHERE category_no=%s", (category_no,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Category already exists")
        else:
            cursor.execute(
                "INSERT INTO category_data VALUES(%s,%s,%s)",
                (category_no, name, description)
            )
            connection.commit()
            messagebox.showinfo("Success", "Category Added Successfully")
            treeview_data()
            clear_fields()
    except Exception as e:
        messagebox.showerror("Database Error", f"{e}")
    finally:
        cursor.close()
        connection.close()


def delete_category():
    selected = category_tree.selection()

    if not selected:
        messagebox.showerror("Error", "Please select a record to delete")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete?")
    if not confirm:
        return

    values = category_tree.item(selected)['values']
    category_no = values[0]

    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute("USE inventory_system")
        cursor.execute("DELETE FROM category_data WHERE category_no=%s", (category_no,))
        connection.commit()

        messagebox.showinfo("Success", "Category Deleted Successfully")
        treeview_data()
        clear_fields()
    except Exception as e:
        messagebox.showerror("Database Error", f"{e}")
    finally:
        cursor.close()
        connection.close()


# ================= CATEGORY FORM =================
def category_form(root):
    global category_no_entry, category_name_entry, description_entry, category_tree

    category_frame = tk.Frame(root, bg='white')
    category_frame.place(x=275, y=100, width=1070, height=580)

    heading = tk.Label(category_frame, text="Manage Category Details",
                       font=('times new roman', 16, 'bold'),
                       bg='#0f4d7d', fg='white')
    heading.place(x=0, y=0, relwidth=1)

    top_frame = tk.Frame(category_frame, bg="white")
    top_frame.place(x=0, y=30, relwidth=1, height=235)
    back_image = tk.PhotoImage(file='arrow.png')
    back_button = tk.Button(top_frame, image=back_image, bd=0, cursor='hand2',
                            command=lambda: category_frame.place_forget(), bg='white')
    back_button.place(x=5, y=20)
    back_button.image = back_image

    img_frame = tk.Frame(category_frame, bg='white')
    img_frame.place(x=40, y=90, width=400, height=450)

    main_image = tk.PhotoImage(file='dairy-products (1).png')
    img_label = tk.Label(img_frame, image=main_image, bg='white')
    img_label.pack()
    img_label.image = main_image

    form_frame = tk.Frame(category_frame, bg='white')
    form_frame.place(x=480, y=90, width=400, height=250)

    tk.Label(form_frame, text='Category No',
             font=('times new roman', 12, 'bold'),
             bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='w')

    category_no_entry = tk.Entry(form_frame,
                                 font=('times new roman', 12, 'bold'),
                                 bg='lightyellow')
    category_no_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(form_frame, text='Category Name',
             font=('times new roman', 12, 'bold'),
             bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')

    category_name_entry = tk.Entry(form_frame,
                                   font=('times new roman', 12, 'bold'),
                                   bg='lightyellow')
    category_name_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(form_frame, text='Description',
             font=('times new roman', 12, 'bold'),
             bg='white').grid(row=2, column=0, padx=10, pady=10, sticky='nw')

    description_entry = tk.Text(form_frame,
                                font=('times new roman', 12, 'bold'),
                                bg='lightyellow',
                                width=25, height=4)
    description_entry.grid(row=2, column=1, padx=10, pady=10)
    # Button frame inside the form
    button_frame = tk.Frame(form_frame, bg='white')
    button_frame.place(x=150, y=180, width=400, height=50)

    # Add button
    tk.Button(button_frame, text='Add',
              width=10, fg='white', bg='#0f4d7d',
              command=add_category).grid(row=0, column=0, padx=10, pady=10)

    # Delete button
    tk.Button(button_frame, text='Delete',
              width=10, fg='white', bg='#0f4d7d',
              command=delete_category).grid(row=0, column=1, padx=10, pady=10)

    table_frame = tk.Frame(category_frame, bg='white')
    table_frame.place(x=480, y=360, width=550, height=200)

    scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
    scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

    category_tree = ttk.Treeview(
        table_frame,
        columns=('no', 'name', 'description'),
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    scroll_y.config(command=category_tree.yview)
    scroll_x.config(command=category_tree.xview)

    category_tree.heading('no', text='Category No')
    category_tree.heading('name', text='Category Name')
    category_tree.heading('description', text='Description')

    category_tree['show'] = 'headings'

    category_tree.column('no', width=100)
    category_tree.column('name', width=150)
    category_tree.column('description', width=250)

    category_tree.pack(fill=tk.BOTH, expand=1)

    category_tree.bind("<ButtonRelease-1>", select_data)

    treeview_data()


