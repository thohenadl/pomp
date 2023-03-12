import tkinter as tk
import os
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
        self.root.config(bg = "#F1F2F2")
        self.style = ttk.Style()
        self.style.configure(
            "AccentButton", 
            foreground = "#F1F2F2", 
            background = "#2B2D42", 
            font       = ("Arial", 12, "bold"), 
            padding    = 10,
        )
        self.style.map(
            "AccentButton", 
            foreground = [
                ("pressed", "#F1F2F2"), 
                ("active", "#F1F2F2")
            ], 
            background = [
                ("pressed", "#3F3F3F"), 
                ("active", "#3F3F3F")
            ]
        )
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
        dropdown.current(0)

        # Create a "Load" button that doesn't perform any action
        ttk.Button(
            master  = self.root, 
            text    = "Load", 
            command = lambda: self.create_widgets(dropdown.get()),
            # style   = "AccentButton",
        ).pack(
            side = tk.LEFT, 
            pady = (0, 30)
        )

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
                master = self.master, 
                text   = errorText,
                fg     = "#FF0000"
            ).pack()
            return
        
        if "pomp_dim" not in self.arr.columns:
            self.arr["pomp_dim"] = ""
        
        self.currentLine = 0
        self.clear_window()

        self.root.grid_propagate(False)
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_columnconfigure(0, weight = 1)

        self.widget_current_line_text()
        self.widget_action_dropdown()
        self.widget_action_buttons(filename)

    def widget_current_line_text(self):
        text = tk.Text(
            self.root,
            bg     = "#ECF0F1",
            fg     = "#34495E",
        )
        text.insert(tk.END, self.arr.iloc[self.currentLine])
        text.grid(column = 0, row = 0, columnspan = 3, sticky='nsew')

    def widget_action_dropdown(self):
        tk.Label(
            master = self.master, 
            text   = "Select action:",
            font   = ("Arial", 12),
            fg     = "#303030",
            bg     = "#f2f2f2",
            padx   = 10,
            pady   = 10,
        ).grid(column = 0, row = 1, sticky='nsew')
        self.dropdown = ttk.Combobox(
            master  = self.master, 
            values  = action_Dimensions,
            font    = ("Arial", 12),
            state   = "readonly",
            justify = "center",
            width   = 30
        )
        self.dropdown.grid(column = 1, row = 1, columnspan = 3, sticky='nsew')
    
    def widget_action_buttons(self, filename):
        ttk.Button(
            master  = self.master, 
            text    = "Submit & go to next line", 
            command = lambda: self.print_input(self.dropdown.get()),
            # style   = "AccentButton",
        ).grid(column = 1, row = 2, sticky='nsew')

        ttk.Button(
            master  = self.master, 
            text    = "Finish & Override file", 
            command = lambda: self.finish_input(filename),
            # style   = "AccentButton",
        ).grid(column = 2, row = 2, sticky='nsew')

    def get_input(self):
        name = self.entry.get()
        print(f"Hello {name}!")

    def run(self):
        self.master.mainloop()

    def print_input(self, action):
        print("Selected Action: ", action)

        if action in action_Dimensions:
            self.arr.loc[self.currentLine, "pomp_dim"] = action
        
        self.currentLine += 1

    def finish_input(self, filename):
        extension = os.path.splitext(filename)[1]

        if extension == ".csv":
            self.arr.to_csv(path_to_files + "/" + log_dir + "/" + filename, index = False)
        elif extension == ".xml":
            self.arr.to_xml(path_to_files + "/" + log_dir + "/" + filename)
        
        self.master.quit()