import tkinter as tk
import numpy as np
import pandas as pd

from tkinter import ttk
from const import *

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1250x500")
        self.master = self.root
        self.master.title("POMP")
        self.result = None

        self.create_file_dropdown()
    
    def create_file_dropdown(self):
        # Create a label for the dropdown
        label = tk.Label(
            master = self.master, 
            text   = "Select a file:"
        )
        label.pack()

        # Get a list of all XML and JSON files in the "logs/uilogs/" directory
        file_list = [f for f in os.listdir(path_to_files + "/" + log_dir + "/") if f.endswith(".xml") or f.endswith(".csv")]

        # Create a dropdown with the file names
        dropdown = ttk.Combobox(
            master = self.master, 
            values = file_list
        )
        dropdown.pack()

        # Create a "Load" button that doesn't perform any action
        button = tk.Button(
            master  = self.master, 
            text    = "Load", 
            command = lambda: self.create_widgets(dropdown.get())
        )
        button.pack()
        
    def clear_window(self):
        # Destroy all child widgets of the window
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_widgets(self, filename):
        extension = os.path.splitext(filename)[1]

        # Create a 2D numpy array
        if extension == ".csv":
            arr = pd.read_csv(
                path_to_files + "/" + log_dir + "/" + filename, 
                sep             = ";", 
                quotechar       = '"', 
                engine          = "python",
                error_bad_lines = False
            )
        elif extension == ".xml":
            arr = pd.read_xml(path_to_files + "/" + log_dir + "/" + filename)
        else:
            # Destroy any existing error labels
            for widget in self.master.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("text").startswith("Error:"):
                    widget.destroy()

            # Unsupported file type
            label = tk.Label(
                master     = self.master, 
                text       = f"Error: Unsupported file type '{extension}'",
                foreground = "#FF0000"
            )
            label.pack()
            return
        
        self.clear_window()

        # Create a Text widget to display the CSV file
        text = tk.Text(self.root)
        text.pack()

        # Read the CSV file and insert its contents into the Text widget
        with open(path_to_files + "/" + log_dir + "/" + filename, 'r') as file:
            contents = file.read()
            text.insert(tk.END, contents)

        text.pack()

        # Create a list of possible actions
        actions = [
            "Open Action", 
            "Navigate Action", 
            "Transform Action", 
            "Transfer Action",
            "Conclude Action", 
            "Close Action", 
            "Empty Action",
        ]

        # Create a dropdown widget with the list of actions
        self.action_var = tk.StringVar(self.master)
        self.action_var.set(actions[0])  # Set the default value
        self.dropdown = tk.OptionMenu(self.master, self.action_var, *actions)
        self.dropdown.pack()

        # Add a submit button to the GUI
        self.submit_button = tk.Button(
            master  = self.master, 
            text    = "Submit", 
            command = self.print_input
        )
        self.submit_button.pack()

        # Add a finish button to the GUI
        self.finish_button = tk.Button(
            master  = self.master, 
            text    = "Finish", 
            command = self.master.quit
        )
        self.finish_button.pack()

    def get_input(self):
        name = self.entry.get()
        print(f"Hello {name}!")

    def run(self):
        self.master.mainloop()

    # Define a function to print the selected action
    def print_input(self):
        action = self.action_var.get()
        print("Selected Action: ", action)