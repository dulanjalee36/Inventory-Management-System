import tkinter as tk
from tkinter import ttk
import pymysql as db
from tkinter import messagebox


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
    if not cursor or not connection:
        return

    cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
    cursor.execute("USE inventory_system")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS supplier_data (
            invoice_no INT PRIMARY KEY,
            name VARCHAR(100),
            contact VARCHAR(30),
            description VARCHAR(180)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM supplier_data")
    count = cursor.fetchone()[0]

   #

    connection.commit()
    cursor.close()
    connection.close()


def supplier_form(root):
    global supplier_treeview, invoice_entry, supplier_entry, contact_entry, description_entry

    create_database_table()

    supplier_frame = tk.Frame(root, bg='white')
    supplier_frame.place(x=275, y=100, width=1070, height=580)

    heading = tk.Label(supplier_frame, text="Manage Supplier Details",
                       font=('times new roman', 16, 'bold'),
                       bg='#0f4d7d', fg='white')
    heading.place(x=0, y=0, relwidth=1)

    top_frame = tk.Frame(supplier_frame, bg="white")
    top_frame.place(x=0, y=30, relwidth=1, height=235)

    back_image = tk.PhotoImage(file='arrow.png')
    back_button = tk.Button(top_frame, image=back_image, bd=0, cursor='hand2',
                            command=lambda: supplier_frame.place_forget(), bg='white')
    back_button.place(x=5, y=20)
    back_button.image = back_image  # keep reference

    form_frame = tk.Frame(supplier_frame, bg='white')
    form_frame.place(x=30, y=90, width=400, height=450)

    tk.Label(form_frame, text='Invoice No', font=('times new roman', 12, 'bold'),
             bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='w')
    invoice_entry = tk.Entry(form_frame, font=('times new roman', 12, 'bold'),
                             bg='lightyellow', state='normal')
    invoice_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(form_frame, text='Supplier Name', font=('times new roman', 12, 'bold'),
             bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')
    supplier_entry = tk.Entry(form_frame, font=('times new roman', 12, 'bold'),
                              bg='lightyellow')
    supplier_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(form_frame, text='Contact', font=('times new roman', 12, 'bold'),
             bg='white').grid(row=2, column=0, padx=10, pady=10, sticky='w')
    contact_entry = tk.Entry(form_frame, font=('times new roman', 12, 'bold'),
                             bg='lightyellow')
    contact_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(form_frame, text='Description', font=('times new roman', 12, 'bold'),
             bg='white').grid(row=3, column=0, padx=10, pady=10, sticky='nw')
    description_entry = tk.Text(form_frame,
                                font=('times new roman', 12, 'bold'),
                                bg='lightyellow',
                                width=25, height=10)
    description_entry.grid(row=3, column=1, padx=10, pady=10)

    show_frame = tk.Frame(supplier_frame, bg='white')
    show_frame.place(x=450, y=70, width=580, height=480)

    # Make show_frame expandable for treeview
    show_frame.rowconfigure(1, weight=1)
    show_frame.columnconfigure(0, weight=1)

    tk.Label(show_frame, text='Search Invoice No:',
             font=('times new roman', 12, 'bold'),
             bg='white').grid(row=0, column=0, padx=5, pady=5)

    search_entry = tk.Entry(show_frame,
                            font=('times new roman', 12, 'bold'),
                            bg='lightyellow')
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(show_frame, text='Search', width=10, fg='white', bg='#0f4d7d',
              command=lambda: search_supplier(search_entry.get())
              ).grid(row=0, column=2, padx=5)

    tk.Button(show_frame, text='Show All', width=10, fg='white', bg='#0f4d7d',
              command=lambda: treeview_data()
              ).grid(row=0, column=3, padx=5)

    hori_scroll = tk.Scrollbar(show_frame, orient='horizontal')
    ver_scroll = tk.Scrollbar(show_frame, orient='vertical')

    supplier_treeview = ttk.Treeview(show_frame,
                                     columns=('invoice_no','name','contact','description'),
                                     show='headings',
                                     xscrollcommand=hori_scroll.set,
                                     yscrollcommand=ver_scroll.set)

    supplier_treeview.grid(row=1, column=0, columnspan=4,
                           sticky='nsew', padx=5, pady=5)

    hori_scroll.grid(row=2, column=0, columnspan=4, sticky='ew')
    ver_scroll.grid(row=1, column=4, sticky='ns')

    hori_scroll.config(command=supplier_treeview.xview)
    ver_scroll.config(command=supplier_treeview.yview)

    supplier_treeview.heading('invoice_no', text='Invoice No')
    supplier_treeview.heading('name', text='Name')
    supplier_treeview.heading('contact', text='Contact')
    supplier_treeview.heading('description', text='Description')

    supplier_treeview.column('invoice_no', width=70)
    supplier_treeview.column('name', width=150)
    supplier_treeview.column('contact', width=100)
    supplier_treeview.column('description', width=250)

    button_frame = tk.Frame(supplier_frame, bg='white')
    button_frame.place(x=50, y=530)

    tk.Button(button_frame, text='Add', width=10, fg='white',
              bg='#0f4d7d', command=lambda: add_supplier()
              ).grid(row=0, column=0, padx=5)

    tk.Button(button_frame, text='Update', width=10, fg='white',
              bg='#0f4d7d', command=lambda: update_supplier()
              ).grid(row=0, column=1, padx=5)

    tk.Button(button_frame, text='Delete', width=10, fg='white',
              bg='#0f4d7d', command=lambda: delete_supplier()
              ).grid(row=0, column=2, padx=5)

    tk.Button(button_frame, text='Clear', width=10, fg='white',
              bg='#0f4d7d', command=lambda: clear_fields()
              ).grid(row=0, column=3, padx=5)

    supplier_treeview.bind('<ButtonRelease-1>', lambda e: select_row())

    # ------------------ FUNCTIONS ------------------ #

    def treeview_data():
        cursor, connection = connect_database()
        if not cursor:
            return
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT * FROM supplier_data")
        rows = cursor.fetchall()
        supplier_treeview.delete(*supplier_treeview.get_children())
        for row in rows:
            supplier_treeview.insert('', tk.END, values=row)
        cursor.close()
        connection.close()

    def add_supplier():
        invoice = invoice_entry.get()
        name = supplier_entry.get()
        contact = contact_entry.get()
        description = description_entry.get("1.0", "end-1c")

        if not invoice or not name or not contact or not description:
            messagebox.showerror("Error", "All fields are required")
            return

        cursor, connection = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("USE inventory_system")
            cursor.execute("SELECT * FROM supplier_data WHERE invoice_no=%s", (invoice,))
            existing = cursor.fetchone()

            if existing:
                messagebox.showerror("Error", f"Invoice No {invoice} already exists!")
            else:
                cursor.execute("INSERT INTO supplier_data VALUES (%s,%s,%s,%s)",
                               (invoice, name, contact, description))
                connection.commit()
                messagebox.showinfo("Success", f"Supplier '{name}' added successfully!")
        except db.Error as e:
            messagebox.showerror("Database Error", f"{e}")
        finally:
            cursor.close()
            connection.close()

        treeview_data()
        clear_fields()

    def update_supplier():
        selected = supplier_treeview.selection()
        if not selected:
            messagebox.showerror("Error", "Select a supplier first")
            return

        old_invoice = supplier_treeview.item(selected[0])['values'][0]
        new_invoice = invoice_entry.get()
        new_name = supplier_entry.get()
        new_contact = contact_entry.get()
        new_description = description_entry.get("1.0", "end-1c")

        if not new_invoice or not new_name or not new_contact or not new_description:
            messagebox.showerror("Error", "All fields are required")
            return

        cursor, connection = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("USE inventory_system")
            if new_invoice != str(old_invoice):
                cursor.execute("SELECT * FROM supplier_data WHERE invoice_no=%s", (new_invoice,))
                if cursor.fetchone():
                    messagebox.showerror("Error", f"Invoice No {new_invoice} already exists!")
                    return

            cursor.execute("""
                UPDATE supplier_data
                SET invoice_no=%s, name=%s, contact=%s, description=%s
                WHERE invoice_no=%s
            """, (new_invoice, new_name, new_contact, new_description, old_invoice))

            connection.commit()
            messagebox.showinfo("Success", f"Supplier '{new_name}' updated successfully!")
        except db.Error as e:
            messagebox.showerror("Database Error", f"{e}")
        finally:
            cursor.close()
            connection.close()

        treeview_data()
        clear_fields()

    def delete_supplier():
        selected = supplier_treeview.selection()
        if not selected:
            messagebox.showerror("Error", "Select a supplier first")
            return

        invoice = supplier_treeview.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Invoice No {invoice}?")
        if not confirm:
            return

        cursor, connection = connect_database()
        if not cursor:
            return

        try:
            cursor.execute("USE inventory_system")
            cursor.execute("DELETE FROM supplier_data WHERE invoice_no=%s", (invoice,))
            connection.commit()
            messagebox.showinfo("Deleted", f"Record with Invoice No {invoice} deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        finally:
            cursor.close()
            connection.close()

        treeview_data()
        clear_fields()

    def search_supplier(invoice_no):
        cursor, connection = connect_database()
        if not cursor:
            return

        cursor.execute("USE inventory_system")
        cursor.execute("SELECT * FROM supplier_data WHERE invoice_no=%s", (invoice_no,))
        rows = cursor.fetchall()

        supplier_treeview.delete(*supplier_treeview.get_children())
        for row in rows:
            supplier_treeview.insert('', tk.END, values=row)

        cursor.close()
        connection.close()

    def select_row():
        selected = supplier_treeview.selection()
        if selected:
            data = supplier_treeview.item(selected[0])['values']

            invoice_entry.config(state='normal')
            invoice_entry.delete(0, tk.END)
            invoice_entry.insert(0, data[0])

            supplier_entry.delete(0, tk.END)
            supplier_entry.insert(0, data[1])

            contact_entry.delete(0, tk.END)
            contact_entry.insert(0, data[2])

            description_entry.delete("1.0", tk.END)
            description_entry.insert(tk.END, data[3])

    def clear_fields():
        invoice_entry.config(state='normal')
        invoice_entry.delete(0, tk.END)

        supplier_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)
        description_entry.delete("1.0", tk.END)

    treeview_data()