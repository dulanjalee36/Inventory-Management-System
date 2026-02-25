import tkinter as tk
from tkinter import ttk, messagebox
import pymysql as db
import random
from datetime import datetime

# ================= GLOBAL VARIABLES =================
product_combo = None
price_value_label = None
quantity_entry = None
bill_tree = None
grand_total_label = None

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
        # Ensure sales_data table exists
        create_tables(cursor)
        return cursor, connection
    except Exception as e:
        messagebox.showerror("Database Error", f"{e}")
        return None, None

# ================= CREATE TABLES IF NOT EXIST =================
def create_tables(cursor):
    # Create sales_data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            bill_no VARCHAR(50),
            product_name VARCHAR(255),
            price DECIMAL(10,2),
            quantity INT,
            total DECIMAL(10,2),
            sale_date DATETIME
        )
    """)
    # Add stock column to product_data if it doesn't exist
    cursor.execute("SHOW COLUMNS FROM product_data LIKE 'stock'")
    if cursor.fetchone() is None:
        cursor.execute("ALTER TABLE product_data ADD COLUMN stock INT DEFAULT 0")

# ================= SALES FORM =================
def sales_form(root):
    global product_combo, price_value_label
    global quantity_entry, bill_tree, grand_total_label

    # MAIN FRAME
    sales_frame = tk.Frame(root, bg='#e6f2ff')
    sales_frame.place(x=275, y=100, width=1070, height=580)

    # TITLE
    tk.Label(
        sales_frame,
        text="SALES MANAGEMENT SYSTEM",
        font=('times new roman', 20, 'bold'),
        bg='#0f4d7d',
        fg='white'
    ).pack(fill=tk.X)

    # LEFT PANEL
    left_frame = tk.Frame(sales_frame, bg='white', bd=3, relief=tk.RIDGE)
    left_frame.place(x=20, y=70, width=350, height=450)

    tk.Label(left_frame, text="Select Product", font=('arial', 12, 'bold'), bg='white').pack(pady=10)
    product_combo = ttk.Combobox(left_frame, font=('arial', 12), state='readonly')
    product_combo.pack(pady=5)

    tk.Label(left_frame, text="Price", font=('arial', 12, 'bold'), bg='white').pack(pady=10)
    price_value_label = tk.Label(left_frame, text="0.00", font=('arial', 12, 'bold'), bg='#fff5cc', width=15)
    price_value_label.pack(pady=5)

    tk.Label(left_frame, text="Quantity", font=('arial', 12, 'bold'), bg='white').pack(pady=10)
    quantity_entry = tk.Entry(left_frame, font=('arial', 12), bg='#e6ffe6')
    quantity_entry.pack(pady=5)

    tk.Button(left_frame, text="Add To Bill", font=('arial', 12, 'bold'), bg='#28a745', fg='white',
              command=add_to_bill).pack(pady=20)

    # RIGHT PANEL
    right_frame = tk.Frame(sales_frame, bg='white', bd=3, relief=tk.RIDGE)
    right_frame.place(x=400, y=70, width=620, height=450)

    columns = ('product', 'price', 'quantity', 'total')
    bill_tree = ttk.Treeview(right_frame, columns=columns, show='headings')
    for col in columns:
        bill_tree.heading(col, text=col.upper())
        bill_tree.column(col, width=140)
    bill_tree.pack(fill=tk.BOTH, expand=1)

    # BOTTOM TOTAL
    grand_total_label = tk.Label(sales_frame, text="Grand Total: 0.00", font=('arial', 14, 'bold'),
                                 bg='#0f4d7d', fg='white')
    grand_total_label.place(x=750, y=540)

    tk.Button(sales_frame, text="Clear Bill", font=('arial', 12, 'bold'), bg='#dc3545', fg='white',
              command=clear_bill).place(x=570, y=535)

    tk.Button(sales_frame, text="Print & Save", font=('arial', 12, 'bold'), bg='#007bff', fg='white',
              command=print_and_save_bill).place(x=430, y=535)

    load_products()

# ================= LOAD PRODUCTS =================
def load_products():
    cursor, connection = connect_database()
    if not cursor:
        return
    cursor.execute("SELECT name FROM product_data")
    rows = cursor.fetchall()
    product_list = [row[0] for row in rows]
    product_combo['values'] = product_list
    product_combo.bind("<<ComboboxSelected>>", get_price)
    cursor.close()
    connection.close()

# ================= GET PRICE =================
def get_price(event):
    selected_product = product_combo.get()
    cursor, connection = connect_database()
    if not cursor:
        return
    cursor.execute("SELECT price FROM product_data WHERE name=%s", (selected_product,))
    result = cursor.fetchone()
    if result:
        price_value_label.config(text=str(result[0]))
    cursor.close()
    connection.close()

# ================= ADD TO BILL =================
def add_to_bill():
    product = product_combo.get()
    price = price_value_label.cget("text")
    quantity = quantity_entry.get()
    if product == "" or quantity == "":
        messagebox.showerror("Error", "Please Select Product and Enter Quantity")
        return
    try:
        total = float(price) * int(quantity)
    except:
        messagebox.showerror("Error", "Invalid Quantity")
        return
    bill_tree.insert('', tk.END, values=(product, price, quantity, total))
    calculate_grand_total()
    quantity_entry.delete(0, tk.END)

# ================= CALCULATE GRAND TOTAL =================
def calculate_grand_total():
    total = 0
    for child in bill_tree.get_children():
        values = bill_tree.item(child, 'values')
        total += float(values[3])
    grand_total_label.config(text=f"Grand Total: {total:.2f}")

# ================= CLEAR BILL =================
def clear_bill():
    bill_tree.delete(*bill_tree.get_children())
    grand_total_label.config(text="Grand Total: 0.00")

# ================= PRINT & SAVE BILL + UPDATE STOCK =================
def print_and_save_bill():
    if not bill_tree.get_children():
        messagebox.showerror("Error", "No items in bill")
        return

    bill_no = f"BILL{random.randint(1000,9999)}"
    cursor, connection = connect_database()
    if not cursor:
        return
    try:
        for child in bill_tree.get_children():
            values = bill_tree.item(child, 'values')
            product, price, qty, total = values
            qty = int(qty)
            price = float(price)
            total = float(total)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # INSERT INTO SALES
            cursor.execute("""
                INSERT INTO sales_data (bill_no, product_name, price, quantity, total, sale_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (bill_no, product, price, qty, total, now))

            # UPDATE STOCK
            cursor.execute("""
                UPDATE product_data SET stock = stock - %s WHERE name = %s
            """, (qty, product))

        connection.commit()
        messagebox.showinfo("Success", f"Bill {bill_no} saved successfully!")

    except Exception as e:
        connection.rollback()
        messagebox.showerror("Database Error", f"Failed to save bill:\n{e}")
    finally:
        cursor.close()
        connection.close()

    # PRINT BILL WINDOW
    bill_window = tk.Toplevel()
    bill_window.title("Bill Receipt")
    bill_window.geometry("500x600")

    tk.Label(bill_window, text="INVOICE", font=('arial', 18, 'bold')).pack()
    tk.Label(bill_window, text=f"Bill No: {bill_no}", font=('arial', 12)).pack()
    text_area = tk.Text(bill_window, width=60, height=20)
    text_area.pack(pady=10)
    text_area.insert(tk.END, "Product\tPrice\tQty\tTotal\n")
    text_area.insert(tk.END, "-"*50 + "\n")
    for child in bill_tree.get_children():
        values = bill_tree.item(child, 'values')
        text_area.insert(tk.END, f"{values[0]}\t{values[1]}\t{values[2]}\t{values[3]}\n")
    text_area.insert(tk.END, "\n" + grand_total_label.cget("text"))

    clear_bill()