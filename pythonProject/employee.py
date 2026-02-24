##Functionality Part
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql as db
from tkinter import messagebox


def select_data(event, empid_entry, Name_entry, email_entry,
                gender_combo, dob_date_entry, contact_entry,
                employment_combo, education_combo, shift_combo, Address_entry,
                doj_date_entry, salary_entry, user_combo, passwrd_entry):
    index = employee_treeview.selection()
    content = employee_treeview.item(index)
    row = content['values']
    clear_feilds(empid_entry, Name_entry, email_entry,
                 gender_combo, dob_date_entry, contact_entry,
                 employment_combo, education_combo, shift_combo, Address_entry,
                 doj_date_entry, salary_entry, user_combo, passwrd_entry, False)

    empid_entry.insert(0, row[0])
    Name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combo.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0, row[5])
    employment_combo.set(row[6])
    education_combo.set(row[7])
    shift_combo.set(row[8])
    Address_entry.insert(1.0, row[9])
    doj_date_entry.set_date(row[10])
    salary_entry.insert(0, row[11])
    user_combo.set(row[12])
    passwrd_entry.insert(0, row[13])


##treeview Function
def treeview_data():
    my_cursor, connection = connect_database()
    if not my_cursor or not connection:
        return
    my_cursor.execute('USE inventory_system')
    try:
        my_cursor.execute('SELECT * FROM employee_data')
        employee_records = my_cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert('', tk.END, values=record)
    except Exception as e:
        tk.messagebox.showerror('Error', f'Error due to {e}')
    finally:
        my_cursor.close()
        connection.close()


##clear button
def clear_feilds(empid_entry, Name_entry, email_entry, gender_combo, dob_date_entry, contact_entry, employment_combo,
                 education_combo, shift_combo, Address_entry,
                 doj_date_entry, salary_entry, user_combo, passwrd_entry, check):
    empid_entry.delete(0, tk.END)
    Name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    from datetime import date
    gender_combo.set('Select Gender')
    dob_date_entry.set_date(date.today())
    contact_entry.delete(0, tk.END)
    employment_combo.set('Select Type')
    education_combo.set('Select Education')
    shift_combo.set('Select Shift')
    Address_entry.delete("1.0", tk.END)
    doj_date_entry.set_date(date.today())
    salary_entry.delete(0, tk.END)
    user_combo.set('Select User Type')
    passwrd_entry.delete(0, tk.END)

    if check:
        employee_treeview.selection_remove(employee_treeview.selection())


##show all button
def show_all():
    treeview_data()


##update Function
def update_employee(empid, name, email, gender, dob, contact,
                    employement_type, education, workshift,
                    address, doj, salary, user_type, password):
    selected = employee_treeview.selection()

    if not selected:
        messagebox.showerror('Error', 'No Select Employee')
        return

    my_cursor, connection = connect_database()
    if not my_cursor or not connection:
        return

    try:
        my_cursor.execute('USE inventory_system')

        # Get current data
        my_cursor.execute('SELECT * FROM employee_data WHERE empid=%s', (empid,))
        current_data = my_cursor.fetchone()

        if not current_data:
            messagebox.showerror('Error', 'Employee not found')
            return

        current_data = current_data[1:]  # remove empid

        new_data = (name, email, gender, dob, contact,
                    employement_type, education, workshift,
                    address, doj, salary, user_type, password)

        if current_data == new_data:
            messagebox.showinfo('Information', 'No changes detected')
            return

        # UPDATE inside try block
        my_cursor.execute('''UPDATE employee_data 
            SET name=%s, email=%s, gender=%s, dob=%s,
                contact=%s, employement_type=%s, education=%s,
                work_shift=%s, address=%s, doj=%s,
                salary=%s, usertype=%s, password=%s
            WHERE empid=%s''',
                          (name, email, gender, dob, contact,
                           employement_type, education, workshift,
                           address, doj, salary, user_type, password, empid))

        connection.commit()

        treeview_data()
        messagebox.showinfo('Success', 'Data is updated Successfully')

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        my_cursor.close()
        connection.close()


##search_button
def search_employee(search_option, value):
    if search_option == 'Search By':
        messagebox.showerror('Error', 'No option selected')
        return
    elif value == '':
        messagebox.showerror('Error', 'Enter the value to search')
        return

    column_mapping = {
        "Id": "empid",
        "Name": "name",
        "E-mail": "email",
        "Type of Employment": "employement_type"
    }

    db_column = column_mapping.get(search_option)
    if not db_column:
        messagebox.showerror('Error', 'Invalid search option')
        return

    my_cursor, connection = connect_database()
    if not my_cursor or not connection:
        return

    try:
        my_cursor.execute('USE inventory_system')

        query = f"SELECT * FROM employee_data WHERE {db_column} LIKE %s"
        my_cursor.execute(query, (f"%{value}%",))
        records = my_cursor.fetchall()

        employee_treeview.delete(*employee_treeview.get_children())

        for record in records:
            employee_treeview.insert('', tk.END, values=record)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        my_cursor.close()
        connection.close()


##delete function
def delete_employee(empid):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', ' No Select Employee')
    else:
        result = messagebox.askyesno('Confirm', 'Do you really want to delete this record ')
        if result:

            my_cursor, connection = connect_database()
            if not my_cursor or not connection:
                return
            try:
                my_cursor.execute('USE inventory_system')
                my_cursor.execute('DELETE FROM employee_data WHERE empid=%s', (empid,))
                connection.commit()
                messagebox.showinfo('Success', 'Data deleted Successfully')
                my_cursor.close()
            except Exception as e:
                (
                    tk.messagebox.showerror('Error', f'Error due to {e}'))
            finally:
                my_cursor.close()
                connection.close()


##database connection

def connect_database():
    try:
        connection = db.connect(
            host='localhost',
            user='root',
            password='12345'
        )
        my_cursor = connection.cursor()

        connection.commit()
        return my_cursor, connection

    except Exception as e:

        messagebox.showerror(
            'Error',
            f'Database connectivity issue:\n{e}'
        )
        return None, None


connect_database()


##create database table
def create_database_table():
    my_cursor, connection = connect_database()

    my_cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
    my_cursor.execute("USE inventory_system")

    my_cursor.execute("""
             CREATE TABLE IF NOT EXISTS employee_data (
                 empid INT(80) PRIMARY KEY,
                 name VARCHAR(100),
                 email VARCHAR(500),
                 gender VARCHAR(50),
                 dob VARCHAR(30),
                 contact VARCHAR(30),
                 employement_type VARCHAR(50),
                 education VARCHAR(50),
                 work_shift VARCHAR(50),
                 address VARCHAR(100),
                 doj VARCHAR(30),
                 salary VARCHAR(50),
                 usertype VARCHAR(50),
                 password VARCHAR(50)
             )
         """)


## delete function


def add_employee(empid, name, email, gender, dob, contact,
                 employment_type, education, workshift,
                 address, doj, salary, user_type, password):
    address = address.strip()

    if (empid == '' or name == '' or email == '' or
            gender == 'Select Gender' or
            contact == '' or
            employment_type == 'Select Type' or
            education == 'Select Education' or
            workshift == 'Select Shift' or
            address == '' or
            user_type == 'Select Usertype' or
            password == ''):
        messagebox.showerror('Error', 'Please enter all fields')
        return

    try:
        my_cursor, connection = connect_database()
        my_cursor.execute("USE inventory_system")

        if not my_cursor or not connection:
            return

        # FIXED SELECT QUERY

        if my_cursor.fetchone():
            messagebox.showerror('Error', 'Id already exists')
            return  # VERY IMPORTANT

        # INSERT QUERY
        my_cursor.execute('SELECT empid FROM employee_data WHERE empid=%s', (empid,))
        if my_cursor.fetchone():
            messagebox.showerror('Error', 'Id already exists')
            return
        address = address.strip()
        my_cursor.execute(
            "INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (empid, name, email, gender, dob, contact,
             employment_type, education, workshift,
             address, doj, salary, user_type, password)
        )

        connection.commit()
        treeview_data()
        messagebox.showinfo('Success', 'Employee data inserted successfully')

    except Exception as e:
        messagebox.showerror('Database Error', str(e))

    finally:
        my_cursor.close()
        connection.close()


def employee_form(root):
    global back_image, employee_treeview
    employee_frame = tk.Frame(root, bg='white')
    employee_frame.place(x=275, y=100, width=1070, height=580)
    headiing_label = tk.Label(employee_frame, text="Manage Employee Details", font=('times new roman', 16, 'bold'),
                              bg='#0f4d7d', fg='white')
    headiing_label.place(x=0, y=0, relwidth=1)

    back_image = tk.PhotoImage(file='arrow.png')

    top_frame = tk.Frame(employee_frame, bg="white")
    top_frame.place(x=0, y=40, relwidth=1, height=235)
    back_button = tk.Button(top_frame, image=back_image, bd=0, cursor='hand2',
                            command=lambda: employee_frame.place_forget(), bg='white')
    back_button.place(x=5, y=0)

    search_frame = tk.Frame(top_frame, bg="white")
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('Id', 'Name', 'E-mail', 'Type of Employment'),
                                   font=('times new roman', 12, 'bold'), state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20, )
    search_entry = tk.Entry(search_frame, font=('times new roman', 12, 'bold'), bg='lightyellow')
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(search_frame, text='Search', font=('times new roman', 12), width=10, cursor='hand2',
                              fg='white', bg='#0f4d7d',
                              command=lambda: search_employee(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)

    show_button = tk.Button(
        search_frame,
        text='Show All',
        font=('times new roman', 12),
        width=10,
        cursor='hand2',
        fg='white',
        bg='#0f4d7d',
        command=show_all
    )
    show_button.grid(row=0, column=3)

    hori_scrollarbar = tk.Scrollbar(top_frame, orient=tk.HORIZONTAL)
    ver_scrollarbar = tk.Scrollbar(top_frame, orient=tk.VERTICAL)

    employee_treeview = ttk.Treeview(top_frame,
                                     columns=('empid', 'name', 'email', 'gender', 'dob', 'contact', 'employment_type',
                                              'education', 'work_shift', 'address', 'doj', 'salary', 'user_type'),
                                     show='headings',
                                     yscrollcommand=ver_scrollarbar.set, xscrollcommand=hori_scrollarbar.set)

    hori_scrollarbar.pack(side=tk.BOTTOM, fill=tk.X)
    ver_scrollarbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(10, 0))
    hori_scrollarbar.config(command=employee_treeview.xview)
    ver_scrollarbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10, 0))

    employee_treeview.heading('empid', text='Employee Id')
    employee_treeview.heading('name', text='Name')
    employee_treeview.heading('email', text='user_email')
    employee_treeview.heading('gender', text='Gender')
    employee_treeview.heading('dob', text='Date of Birth')
    employee_treeview.heading('contact', text='Contact')
    employee_treeview.heading('employment_type', text='Type of Employment')
    employee_treeview.heading('education', text='Education')
    employee_treeview.heading('work_shift', text='Work Shift')
    employee_treeview.heading('address', text='Address')
    employee_treeview.heading('doj', text='Date of Joining')
    employee_treeview.heading('salary', text='Salary')
    employee_treeview.heading('user_type', text='User Type')

    employee_treeview.column('empid', width=60)
    employee_treeview.column('name', width=140)
    employee_treeview.column('email', width=180)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('dob', width=100)
    employee_treeview.column('contact', width=100)
    employee_treeview.column('employment_type', width=120)
    employee_treeview.column('education', width=120)
    employee_treeview.column('work_shift', width=120)
    employee_treeview.column('address', width=200)
    employee_treeview.column('doj', width=100)
    employee_treeview.column('salary', width=140)
    employee_treeview.column('user_type', width=140)

    treeview_data()

    detail_frame = tk.Frame(employee_frame, bg="white")

    detail_frame.place(x=30, y=320, )

    empid_label = tk.Label(detail_frame, text='Employee ID', font=('times new roman', 12, 'bold'), bg="white")
    empid_label.grid(row=0, column=0, padx=20, pady=10, sticky='W')
    empid_entry = tk.Entry(detail_frame, font=('times new roman', 12, 'bold'), bg="lightyellow")
    empid_entry.grid(row=0, column=1, padx=20, pady=10)

    Name_label = tk.Label(detail_frame, text='Name', font=('times new roman', 12, 'bold'), bg="white")
    Name_label.grid(row=0, column=2, padx=20, pady=10, sticky='W')
    Name_entry = tk.Entry(detail_frame, font=('times new roman', 12, 'bold'), bg="lightyellow")
    Name_entry.grid(row=0, column=3, padx=20, pady=10)

    email_label = tk.Label(detail_frame, text='Email', font=('times new roman', 12, 'bold'), bg="white")
    email_label.grid(row=0, column=4, padx=20, pady=10, sticky='W')
    email_entry = tk.Entry(detail_frame, font=('times new roman', 12, 'bold'), bg="lightyellow")
    email_entry.grid(row=0, column=5, padx=20, pady=10)

    gender_label = tk.Label(detail_frame, text='Gender', font=('times new roman', 12, 'bold'), bg="white")
    gender_label.grid(row=1, column=0, padx=20, pady=10, sticky='W')
    gender_combo = ttk.Combobox(
        detail_frame,
        values=("Male", "Female"),
        font=('times new roman', 12, 'bold'), width=18, state='readonly'
    )
    gender_combo.set('Select Gender')
    gender_combo.grid(row=1, column=1, padx=20, pady=10)

    dob_label = tk.Label(detail_frame, text='Date of Birth', font=('times new roman', 12, 'bold'), bg="white")
    dob_label.grid(row=1, column=2, padx=20, pady=10, sticky='W')

    dob_date_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12, 'bold'), state='readonly',
                               date_pattern='DD/MM/YY')
    dob_date_entry.grid(row=1, column=3, padx=20, pady=10)

    contact_label = tk.Label(detail_frame, text='Contact', font=('times new roman', 12, 'bold'), bg="white")
    contact_label.grid(row=1, column=4, padx=20, pady=10, sticky='W')
    contact_entry = tk.Entry(detail_frame, font=('times new roman', 12, 'bold'), bg="lightyellow")
    contact_entry.grid(row=1, column=5, padx=20, pady=10)

    employment_label = tk.Label(detail_frame, text='Employment Type', font=('times new roman', 12, 'bold'), bg="white")
    employment_label.grid(row=2, column=0, padx=20, pady=10, sticky='W')
    employment_combo = ttk.Combobox(
        detail_frame,
        values=("Full Time", "Part Time", "Casual", "Contract", "Intern"),
        font=('times new roman', 12, 'bold'), width=18, state='readonly'
    )
    employment_combo.set('Select Type')
    employment_combo.grid(row=2, column=1, padx=20, pady=10)

    education_label = tk.Label(detail_frame, text='Education', font=('times new roman', 12, 'bold'), bg="white")
    education_label.grid(row=2, column=2, padx=20, pady=10, sticky='W')
    education_combo = ttk.Combobox(
        detail_frame,
        values=("B.Tech", "B.Com", "M.Tech", "M.Com", "B.Sc", "M.Sc", "BBA", "MBA", "LLB", "LLM", "B.Arch"),
        font=('times new roman', 12, 'bold'), width=18, state='readonly'
    )
    education_combo.set('Select Education')
    education_combo.grid(row=2, column=3, padx=20, pady=10)

    shift_label = tk.Label(detail_frame, text='Work Shift', font=('times new roman', 12, 'bold'), bg="white")
    shift_label.grid(row=2, column=4, padx=20, pady=10, sticky='W')
    shift_combo = ttk.Combobox(
        detail_frame,
        values=("Morning", "Evening", "Night"),
        font=('times new roman', 12, 'bold'), width=18, state='readonly'
    )
    shift_combo.set('Select Shift')
    shift_combo.grid(row=2, column=5, padx=20, pady=10)

    Address_label = tk.Label(detail_frame, text='City', font=('times new roman', 12, 'bold'), bg="white")
    Address_label.grid(row=3, column=0, padx=20, pady=10, sticky='W')
    Address_entry = tk.Text(detail_frame, font=('times new roman', 12, 'bold'), bg="lightyellow", width=20, height=3)
    Address_entry.grid(row=3, column=1, padx=20, pady=10, rowspan=2)

    doj_label = tk.Label(detail_frame, text='Date of Joining', font=('times new roman', 12, 'bold'), bg="white")
    doj_label.grid(row=3, column=2, padx=20, pady=10, sticky='W')

    doj_date_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12, 'bold'), state='readonly',
                               date_pattern='DD/MM/YY')
    doj_date_entry.grid(row=3, column=3, padx=20, pady=10)

    passwrd_label = tk.Label(detail_frame, text='Password', font=('times new roman', 12, 'bold'), bg="white")
    passwrd_label.grid(row=4, column=4, padx=20, pady=10, sticky='W')
    passwrd_entry = tk.Entry(detail_frame, font=('times new roman', 12, 'bold'), bg="lightyellow")
    passwrd_entry.grid(row=4, column=5, padx=20, pady=10)

    salary_label = tk.Label(detail_frame, text='Salary', font=('times new roman', 12, 'bold'), bg="white")
    salary_label.grid(row=3, column=4, padx=20, pady=10, sticky='W')
    salary_entry = tk.Entry(detail_frame, font=('times new roman', 12, 'bold'), bg="lightyellow")
    salary_entry.grid(row=3, column=5, padx=20, pady=10)

    user_label = tk.Label(detail_frame, text='User Type', font=('times new roman', 12, 'bold'), bg="white")
    user_label.grid(row=4, column=2, padx=20, pady=10, sticky='W')
    user_combo = ttk.Combobox(
        detail_frame,
        values=("Employee", "Admin"),
        font=('times new roman', 12, 'bold'), width=18, state='readonly'
    )
    user_combo.set('Select Usertype')
    user_combo.grid(row=4, column=3, padx=20, pady=10)

    button_Frame = tk.Frame(employee_frame, bg="white")
    button_Frame.place(x=200, y=550)

    add_button = tk.Button(button_Frame, text='ADD', font=('times new roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d',
                           command=lambda: add_employee(empid_entry.get(), Name_entry.get(), email_entry.get(),
                                                        gender_combo.get(),
                                                        dob_date_entry.get(), contact_entry.get(),
                                                        employment_combo.get(),
                                                        education_combo.get(), shift_combo.get(),
                                                        Address_entry.get("1.0", "end-1c"),
                                                        doj_date_entry.get(), salary_entry.get(), user_combo.get(),
                                                        passwrd_entry.get()))
    add_button.grid(row=0, column=2, padx=20, sticky='W')

    Update_button = tk.Button(button_Frame, text='Update', font=('times new roman', 12), width=10, cursor='hand2',
                              fg='white', bg='#0f4d7d',
                              command=lambda: update_employee(empid_entry.get(), Name_entry.get(), email_entry.get(),
                                                              gender_combo.get(),
                                                              dob_date_entry.get(), contact_entry.get(),
                                                              employment_combo.get(),
                                                              education_combo.get(), shift_combo.get(),
                                                              Address_entry.get("1.0", "end-1c"),
                                                              doj_date_entry.get(), salary_entry.get(),
                                                              user_combo.get(), passwrd_entry.get()))
    Update_button.grid(row=0, column=3, padx=20, sticky='W')

    delete_button = tk.Button(button_Frame, text='Delete', font=('times new roman', 12), width=10, cursor='hand2',
                              fg='white', bg='#0f4d7d', command=lambda: delete_employee(empid_entry.get()))
    delete_button.grid(row=0, column=4, padx=20, sticky='W')
    Clear_button = tk.Button(button_Frame, text='Clear', font=('times new roman', 12), width=10, cursor='hand2',
                             fg='white', bg='#0f4d7d',
                             command=lambda: clear_feilds(empid_entry, Name_entry, email_entry, gender_combo,
                                                          dob_date_entry, contact_entry, employment_combo,
                                                          education_combo, shift_combo, Address_entry,
                                                          doj_date_entry, salary_entry, user_combo, passwrd_entry,
                                                          True))
    Clear_button.grid(row=0, column=5, padx=20, sticky='W')
    employee_treeview.bind('<ButtonRelease-1>',
                           lambda event: select_data(event, empid_entry, Name_entry, email_entry, gender_combo,
                                                     dob_date_entry, contact_entry, employment_combo,
                                                     education_combo, shift_combo, Address_entry,
                                                     doj_date_entry, salary_entry, user_combo, passwrd_entry))

    create_database_table()

