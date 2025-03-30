import customtkinter as ctk
from view.viewInterface import MainInterface

ctk.set_appearance_mode("dark")
# Create main window
root = ctk.CTk()

# Create instance for main interface
interface = MainInterface(root)

# Configure size and title
root.geometry("1024x768")
root.title("Treasury control")

# Start app
root.mainloop()