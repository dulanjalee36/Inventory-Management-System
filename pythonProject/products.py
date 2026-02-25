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
            password='12345',
            database='inventory_system'
        )
        cursor = connection.cursor()
        return cursor, connection
    except Exception as e:
        messagebox.showerror("Database Error", f"{e}")
        return None, None


# ================= CREATE DATABASE & TABLE =================
def create_database_table():
    try:
        connection = db.connect(
            host='localhost',
            user='root',
            password='12345'
        )
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
        cursor.execute("USE inventory_system")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_data(
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(100),
                supplier VARCHAR(100),
                name VARCHAR(100),
                price DOUBLE,
                quantity INT,
                status VARCHAR(50)
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        messagebox.showerror("Database Error", f"{e}")


# ================= FUNCTIONS =================
def treeview_data():
    cursor, connection = connect_database()
    if not cursor:
        return

    cursor.execute("SELECT * FROM product_data")
    rows = cursor.fetchall()

    product_tree.delete(*product_tree.get_children())

    for row in rows:
        product_tree.insert('', tk.END, values=row)

    cursor.close()
    connection.close()


def clear_fields():
    category_entry.delete(0, tk.END)
    supplier_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)


# ✅ FIXED SELECTION FUNCTION
def select_data(event):
    selected = product_tree.focus()

    if selected == "":
        return

    values = product_tree.item(selected, 'values')

    category_entry.delete(0, tk.END)
    category_entry.insert(0, values[1])

    supplier_entry.delete(0, tk.END)
    supplier_entry.insert(0, values[2])

    name_entry.delete(0, tk.END)
    name_entry.insert(0, values[3])

    price_entry.delete(0, tk.END)
    price_entry.insert(0, values[4])

    quantity_entry.delete(0, tk.END)
    quantity_entry.insert(0, values[5])

    status_entry.delete(0, tk.END)
    status_entry.insert(0, values[6])


def add_product():
    if category_entry.get() == "" or supplier_entry.get() == "" or \
       name_entry.get() == "" or price_entry.get() == "" or \
       quantity_entry.get() == "" or status_entry.get() == "":
        messagebox.showerror("Error", "All Fields Are Required")
        return

    cursor, connection = connect_database()
    if not cursor:
        return

    try:
        cursor.execute("""
            INSERT INTO product_data(category, supplier, name, price, quantity, status)
            VALUES(%s,%s,%s,%s,%s,%s)
        """, (
            category_entry.get(),
            supplier_entry.get(),
            name_entry.get(),
            price_entry.get(),
            quantity_entry.get(),
            status_entry.get()
        ))

        connection.commit()
        messagebox.showinfo("Success", "Product Added Successfully")

        treeview_data()
        clear_fields()

    except Exception as e:
        messagebox.showerror("Database Error", f"{e}")

    finally:
        cursor.close()
        connection.close()


# ✅ FIXED DELETE FUNCTION
def delete_product():
    selected = product_tree.focus()

    if selected == "":
        messagebox.showerror("Error", "Please Select a Record")
        return

    values = product_tree.item(selected, 'values')
    product_id = values[0]

    confirm = messagebox.askyesno("Confirm", "Delete selected product?")
    if not confirm:
        return

    cursor, connection = connect_database()

    try:
        cursor.execute("DELETE FROM product_data WHERE product_id=%s", (product_id,))
        connection.commit()

        product_tree.delete(selected)

        messagebox.showinfo("Success", "Product Deleted Successfully")
        clear_fields()

    except Exception as e:
        messagebox.showerror("Database Error", f"{e}")

    finally:
        cursor.close()
        connection.close()


# ================= PRODUCT FORM =================
def product_form(root):

    create_database_table()

    global category_entry, supplier_entry, name_entry
    global price_entry, quantity_entry, status_entry
    global product_tree

    product_frame = tk.Frame(root, bg='white')
    product_frame.place(x=275, y=100, width=1070, height=580)

    heading = tk.Label(product_frame, text="Manage Product Details",
                       font=('times new roman', 16, 'bold'),
                       bg='#0f4d7d', fg='white')
    heading.place(x=0, y=0, relwidth=1)

    top_frame = tk.Frame(product_frame, bg="white")
    top_frame.place(x=0, y=30, relwidth=1, height=235)
    back_image = tk.PhotoImage(file='arrow.png')
    back_button = tk.Button(top_frame, image=back_image, bd=0, cursor='hand2',
                            command=lambda: product_frame.place_forget(), bg='white')
    back_button.place(x=5, y=20)
    back_button.image = back_image

    # ===== Form Frame =====
    form_frame = tk.Frame(product_frame, bg='white')
    form_frame.place(x=20, y=80, width=450, height=350)

    labels = ['Category', 'Supplier', 'Name', 'Price', 'Quantity', 'Status']

    for i, text in enumerate(labels):
        tk.Label(form_frame, text=text,
                 font=('times new roman', 12, 'bold'),
                 bg='white').grid(row=i, column=0, padx=10, pady=8, sticky='w')

    category_entry = tk.Entry(form_frame, font=('times new roman', 12), bg='lightyellow')
    supplier_entry = tk.Entry(form_frame, font=('times new roman', 12), bg='lightyellow')
    name_entry = tk.Entry(form_frame, font=('times new roman', 12), bg='lightyellow')
    price_entry = tk.Entry(form_frame, font=('times new roman', 12), bg='lightyellow')
    quantity_entry = tk.Entry(form_frame, font=('times new roman', 12), bg='lightyellow')
    status_entry = tk.Entry(form_frame, font=('times new roman', 12), bg='lightyellow')

    entries = [category_entry, supplier_entry, name_entry,
               price_entry, quantity_entry, status_entry]

    for i, entry in enumerate(entries):
        entry.grid(row=i, column=1, padx=10, pady=8)

    # ===== Buttons =====
    button_frame = tk.Frame(form_frame, bg='white')
    button_frame.grid(row=6, column=0, columnspan=2, pady=15)

    tk.Button(button_frame, text='Add', width=10,
              fg='white', bg='#0f4d7d',
              command=add_product).grid(row=0, column=0, padx=5)

    tk.Button(button_frame, text='Delete', width=10,
              fg='white', bg='#0f4d7d',
              command=delete_product).grid(row=0, column=1, padx=5)

    tk.Button(button_frame, text='Clear', width=10,
              fg='white', bg='#0f4d7d',
              command=clear_fields).grid(row=0, column=2, padx=5)

    # ===== Treeview =====
    table_frame = tk.Frame(product_frame, bg='white')
    table_frame.place(x=500, y=50, width=550, height=500)

    scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
    scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

    product_tree = ttk.Treeview(
        table_frame,
        columns=('id', 'category', 'supplier', 'name', 'price', 'quantity', 'status'),
        show='headings',
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    scroll_y.config(command=product_tree.yview)
    scroll_x.config(command=product_tree.xview)

    columns = ['id', 'category', 'supplier', 'name', 'price', 'quantity', 'status']
    widths = [50, 100, 100, 100, 80, 80, 80]

    for col, width in zip(columns, widths):
        product_tree.heading(col, text=col.capitalize())
        product_tree.column(col, width=width)

    product_tree.pack(fill=tk.BOTH, expand=1)

    # ✅ PROFESSIONAL SELECTION EVENT
    product_tree.bind("<<TreeviewSelect>>", select_data)

    treeview_data()