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
        self.currentLine = 0

        self.create_file_dropdown()
    
    def create_file_dropdown(self):
        # Create a label for the dropdown
        label = tk.Label(
            master = self.root, 
            text   = "Select a file:",
            font   = ("Arial", 14),
            fg     = "#303030",
            bg     = "#f2f2f2",
            padx   = 10,
            pady   = 10,
        )
        label.pack(
            side   = tk.TOP, 
            anchor = tk.NW
        )

        # Get a list of all XML and JSON files in the "logs/uilogs/" directory
        file_list = [f for f in os.listdir(path_to_files + "/" + log_dir + "/") if f.endswith(".xml") or f.endswith(".csv")]

        # Create a dropdown with the file names
        dropdown_frame = tk.Frame(self.root, bg = "#f2f2f2")
        dropdown_frame.pack(
            padx = 10, 
            pady = 10, 
            fill = tk.X
        )

        tk.Label(
            master = dropdown_frame, 
            text   = "Select file:",
            font   = ("Arial", 12),
            fg     = "#303030",
            bg     = "#f2f2f2",
            padx   = 10,
            pady   = 10,
        ).pack(side = tk.LEFT)

        dropdown = ttk.Combobox(
            master = dropdown_frame, 
            values = file_list,
            font   = ("Arial", 12),
            width  = 30,
        )
        dropdown.pack(
            side = tk.LEFT, 
            padx = 10
        )

        # Create a "Load" button that doesn't perform any action
        button_frame = tk.Frame(self.root, bg = "#f2f2f2")
        button_frame.pack(
            padx = 10, 
            pady = 10, 
            fill = tk.X
        )

        tk.Button(
            master  = button_frame, 
            text    = "Load", 
            font    = ("Arial", 12),
            bg      = "#303030",
            fg      = "#f2f2f2",
            padx    = 10,
            pady    = 10,
            command = lambda: self.create_widgets(dropdown.get())
        ).pack(side = tk.RIGHT)

        # Add some padding at the bottom of the window
        tk.Frame(
            self.root, 
            height = 20, 
            bg     = "#f2f2f2"
        ).pack(fill = tk.X)
        
    def clear_window(self):
        # Destroy all child widgets of the window
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_widgets(self, filename):
        extension = os.path.splitext(filename)[1]

        # Create a 2D numpy array
        if extension == ".csv":
            self.arr = pd.read_csv(
                path_to_files + "/" + log_dir + "/" + filename, 
                sep             = ";", 
                quotechar       = '"', 
                engine          = "python",
                error_bad_lines = False
            )
        elif extension == ".xml":
            self.arr = pd.read_xml(path_to_files + "/" + log_dir + "/" + filename)
        else:
            # Destroy any existing error labels
            for widget in self.master.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("text").startswith("Error:"):
                    widget.destroy()

            if len(extension) > 0:
                errorText = f"Error: Unsupported file type '{extension}'"
            else:
                errorText = "Error: You need to select a file"

            # Unsupported file type
            tk.Label(
                master     = self.master, 
                text       = errorText,
                foreground = "#FF0000"
            ).pack()
            return
        
        if "pomp_dim" not in self.arr.columns:
            self.arr["pomp_dim"] = ""
        
        self.currentLine = 0
        self.clear_window()

        # Create a Text widget to display the CSV file
        text = tk.Text(self.root)
        text.insert(tk.END, self.arr.iloc[self.currentLine])
        text.pack()

        # Create a dropdown widget with the list of actions
        self.dropdown = ttk.Combobox(
            master = self.master, 
            values = action_Dimensions
        )
        self.dropdown.pack()

        # Add a submit button to the GUI
        self.submit_button = tk.Button(
            master  = self.master, 
            text    = "Submit & go to next line", 
            command = lambda: self.print_input(self.dropdown.get())
        )
        self.submit_button.pack()

        # Add a finish button to the GUI
        self.finish_button = tk.Button(
            master  = self.master, 
            text    = "Finish & Override file", 
            command = lambda: self.finish_input(filename)
        )
        self.finish_button.pack()

    def get_input(self):
        name = self.entry.get()
        print(f"Hello {name}!")

    def run(self):
        self.master.mainloop()

    # Define a function to print the selected action
    def print_input(self, action):
        print("Selected Action: ", action)

        if action in action_Dimensions:
            self.arr.loc[self.currentLine, "pomp_dim"] = action
        print(self.arr.iloc[self.currentLine])
        self.currentLine += 1

    def finish_input(self, filename):
        extension = os.path.splitext(filename)[1]

        if extension == ".csv":
            self.arr.to_csv(path_to_files + "/" + log_dir + "/" + filename, index = False)
        elif extension == ".xml":
            self.arr.to_xml(path_to_files + "/" + log_dir + "/" + filename)
        
        self.master.quit()