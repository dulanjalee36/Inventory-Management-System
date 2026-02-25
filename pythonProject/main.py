import tkinter as tk
from tkinter import ttk, messagebox
import time
import pymysql
import subprocess  # Added to handle relaunching the login page
import sys         # Added to get the python path

# ================= MODULE IMPORTS =================
try:
    from employee import employee_form
    from suplier import supplier_form
    from category import category_form
    from products import product_form
    from sales import sales_form
    from exit import exit_app
except ImportError as e:
    print(f"Module Import Error: {e}")


# ================= DATABASE CONNECTION =================
def get_connection():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='12345',
            database='inventory_system'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", f"Connection Error: {str(e)}")
        return None


def get_table_count(table_name):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
        except:
            count = 0
        finally:
            conn.close()
        return count
    return 0


# ================= MAIN DASHBOARD WINDOW =================
def open_dashboard():
    root = tk.Tk()
    root.title('Inventory Management System | Dashboard')
    root.geometry('1350x710+0+0')
    root.resizable(False, False)
    root.config(bg='#f4f7f6')

    # ================= TITLE HEADER =================
    header_height = 65
    try:
        logo_img = tk.PhotoImage(file='inventory.png')
    except:
        logo_img = None

    titleLabel = tk.Label(root, image=logo_img, compound=tk.LEFT,
                          text='  Inventory Management System',
                          font=('Arial', 35, 'bold'),
                          bg='#010c48', fg='white', anchor='w', padx=20)
    titleLabel.image = logo_img
    titleLabel.place(x=0, y=0, relwidth=1, height=header_height)

    # ================= DATE & TIME =================
    subtitle_height = 35

    def update_time():
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%d-%m-%Y")
        subTitleLabel.config(text=f'Welcome Admin\t\t Date: {current_date}\t\t Time: {current_time}')
        subTitleLabel.after(1000, update_time)

    subTitleLabel = tk.Label(root, font=('Arial', 14), bg='#4d636d', fg='white')
    subTitleLabel.place(x=0, y=header_height, relwidth=1, height=subtitle_height)
    update_time()

    # ================= LOGOUT FUNCTION =================
    # FIXED: Re-launching the login script correctly
    def logout_action(current_window):
        answer = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if answer:
            current_window.destroy()  # Close dashboard
            # Relaunch login.py as a new process
            subprocess.Popen([sys.executable, "login.py"])

    # ================= LOGOUT BUTTON =================
    logout_btn = tk.Button(
        root,
        text='Logout',
        font=('Arial', 14, 'bold'),
        fg='#010c48',
        bg='#5DCFBC',
        cursor="hand2",
        command=lambda: logout_action(root)
    )
    logout_btn.place(x=1200, y=12, width=110, height=40)

    # ================= LEFT SIDE MENU =================
    leftFrame = tk.Frame(root, bg='white', bd=2, relief=tk.RIDGE)
    leftFrame.place(x=0, y=100, width=275, height=585)

    try:
        inven_img = tk.PhotoImage(file='inventory (1).png')
        imageLabel = tk.Label(leftFrame, image=inven_img, bg="white", bd=0, highlightthickness=0)
        imageLabel.image = inven_img
        imageLabel.pack(side=tk.TOP, fill=tk.X, pady=0)
    except:
        pass

    tk.Label(leftFrame, text='MAIN MENU', font=('Arial', 18, 'bold'),
             bg='#009688', fg='white', pady=10).pack(fill=tk.X)

    def create_menu_button(image_file, text, command):
        try:
            img = tk.PhotoImage(file=image_file)
        except:
            img = None
        btn = tk.Button(leftFrame, image=img, compound=tk.LEFT, text='  ' + text,
                        font=('Arial', 16, 'bold'), anchor="w", padx=15,
                        bg="white", bd=1, relief=tk.GROOVE, cursor="hand2", command=command)
        btn.image = img
        btn.pack(fill=tk.X, pady=0)

    create_menu_button('man (1).png', 'Employees', lambda: employee_form(root))
    create_menu_button('supplier.png', 'Suppliers', lambda: supplier_form(root))
    create_menu_button('categorization.png', 'Category', lambda: category_form(root))
    create_menu_button('product.png', 'Products', lambda: product_form(root))
    create_menu_button('sales.png', 'Sales', lambda: sales_form(root))
    create_menu_button('logout.png', 'Exit', lambda: exit_app(root))

    # ================= DASHBOARD CONTENT AREA =================
    card_container = tk.Frame(root, bg='#f4f7f6')
    card_container.place(x=280, y=130, width=1050, height=550)

    card_container.grid_columnconfigure(0, weight=1)
    card_container.grid_columnconfigure(1, weight=1)

    cards_data = [
        ('#2c3e50', 'staff.png', 'Total Employees', get_table_count("employee_data")),
        ('#8e44ad', 'supplier (1).png', 'Total Suppliers', get_table_count("supplier_data")),
        ('#27AE60', 'market-segment.png', 'Total Categories', get_table_count("category_data")),
        ('#d35400', 'products.png', 'Total Products', get_table_count("product_data")),
        ('#c0392b', 'trend.png', 'Total Sales', get_table_count("sales_data")),
    ]

    for i, (bg_col, img_f, title_t, val) in enumerate(cards_data):
        r, c, span = (0, i, 1) if i < 2 else (1, i - 2, 1) if i < 4 else (2, 0, 2)

        f = tk.Frame(card_container, bg=bg_col, bd=0, relief=tk.RIDGE, width=450, height=160)
        f.grid(row=r, column=c, columnspan=span, padx=15, pady=15)
        f.grid_propagate(False)

        try:
            img = tk.PhotoImage(file=img_f)
            tk.Label(f, image=img, bg=bg_col).place(x=30, y=35)
            f.image = img
        except:
            pass

        tk.Label(f, text=title_t, font=('Arial', 20, 'bold'), fg='white', bg=bg_col).place(x=150, y=40)
        tk.Label(f, text=str(val), font=('Arial', 40, 'bold'), fg='white', bg=bg_col).place(x=150, y=85)

    tk.Label(root, text="Inventory Management System | © 2026 Admin Portal",
             font=("Arial", 10), bg="#4d636d", fg="white").pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()

