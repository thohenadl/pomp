import tkinter as tk
import numpy as np
import pandas as pd

from const import *

class MyGUI:
    def __init__(self,filename):
        self.root = tk.Tk()
        self.root.geometry("1250x500")
        self.master = self.root
        self.master.title(str(filename))

        self.filename = filename
        self.result = None

        self.create_widgets()
        
    def create_widgets(self):
        # Create a 2D numpy array
        arr = pd.read_csv(path_to_files + "/" + log_dir + "/" + self.filename, sep=";", quotechar='"', engine="python",
                            error_bad_lines=False)

        # Create a Text widget to display the CSV file
        text = tk.Text(self.root)
        text.pack()

        # Read the CSV file and insert its contents into the Text widget
        with open(path_to_files + "/" + log_dir + "/" + self.filename, 'r') as file:
            contents = file.read()
            text.insert(tk.END, contents)

        text.pack()

        # Create a list of possible actions
        actions = ["Open Action", "Navigate Action", "Transform Action", "Transfer Action",
                   "Conclude Action", "Close Action", "Empty Action"]

        # Create a dropdown widget with the list of actions
        self.action_var = tk.StringVar(self.master)
        self.action_var.set(actions[0])  # Set the default value
        self.dropdown = tk.OptionMenu(self.master, self.action_var, *actions)
        self.dropdown.pack()

        # Add a submit button to the GUI
        self.submit_button = tk.Button(self.master, text="Submit", command=self.print_input)
        self.submit_button.pack()

        # Add a finish button to the GUI
        self.finish_button = tk.Button(self.master, text="Finish", command=self.master.quit)
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