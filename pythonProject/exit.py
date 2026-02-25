from tkinter import messagebox

def exit_app(root):
    """Show confirmation and exit the application"""
    answer = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if answer:
        root.destroy()  # Clo