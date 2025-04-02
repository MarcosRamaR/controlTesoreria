import customtkinter as ctk
from view.viewInterface import MainInterface

def on_closing():
    root.quit()
    root.destroy()

ctk.set_appearance_mode("dark")
# Create main window
root = ctk.CTk()
root.protocol("WM_DELETE_WINDOW", on_closing) #Handle the closing

# Create instance for main interface
interface = MainInterface(root)

# Configure size and title
root.geometry("1024x768")
root.title("Treasury control")

# Start app
root.mainloop()