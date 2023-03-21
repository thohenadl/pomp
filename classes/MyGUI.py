import tkinter as tk
import os
import pandas as pd
import time

from tkinter import ttk
from const import *
from util.csvUtil import store_log
from util.tagging import tag_UI_w_POMP

class MyGUI:
    def __init__(self):
        self.hideNAN_state = False
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
        file_list = [f for f in os.listdir(path_to_files + "/" + pomp_tagged_dir + "/") if f.endswith(".xml") or f.endswith(".csv")]

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
                path_to_files + "/" + pomp_tagged_dir + "/" + filename, 
                sep             = ";", 
                quotechar       = '"', 
                engine          = "python",
                error_bad_lines = False
            )
        elif extension == ".xml":
            self.arr = pd.read_xml(path_to_files + "/" + pomp_tagged_dir + "/" + filename)
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
        """
        Function does display the current line of the UI log

        Args:
            state (bool): True if NAN values should be removed

        Returns:
            -
        """
        text = tk.Text(
            self.root,
            bg     = "#ECF0F1",
            fg     = "#34495E",
        )
        if self.currentLine < len(self.arr):
            if self.hideNAN_state:
                text.insert(tk.END, self.arr.iloc[self.currentLine].dropna())
            else:
                text.insert(tk.END, self.arr.iloc[self.currentLine])
        else:
            text.insert(tk.END, "All rows in selcted file have been tagged.")
            # Solves issue #12 https://github.com/thohenadl/pomp/issues/12
            self.set_button_state(self.button_tag,"disabled")
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
        self.button_tag = ttk.Button(
            master  = self.master, 
            text    = "Submit & go to next line", 
            command = lambda: (
                self.print_input(self.dropdown.get()),
                # Solves Issue #11 - https://github.com/thohenadl/pomp/issues/11
                self.widget_current_line_text()
            ),
        # style   = "AccentButton",
        )
        self.button_tag.grid(column = 1, row = 2, sticky='nsew')

        self.button_finish = ttk.Button(
            master  = self.master, 
            text    = "Finish & Override file", 
            command = lambda: self.finish_input(filename),
            # style   = "AccentButton",
            )
        self.button_finish.grid(column = 2, row = 2, sticky='nsew')

        self.button_hideNAN = ttk.Button(
            master = self.master,
            text = "Hide NAN Values",
            command = lambda: (
                self.change_HideNAN_state(),
                self.widget_current_line_text()
            )
        # style   = "AccentButton",
        )
        self.button_hideNAN.grid(column = 3, row = 2, sticky='nsew')

    def change_HideNAN_state(self):
        if self.hideNAN_state:
            self.hideNAN_state = False
            self.button_hideNAN['text'] = "Hide NAN Values"
        else:
            self.hideNAN_state = True
            self.button_hideNAN['text'] = "Show NAN Values"

    def set_button_state(self, button: object, state: str):
        """
        Method to disable the "Set Tag/Next Line" Button

        Args:
            state (str): "normal" for active and "disabled" for inactive state
            button (object): Hand over the button that should be disabled
        Returns:
            -

        Raises:
            NameError, if button does not exist
        """
        # Solves issue #12 https://github.com/thohenadl/pomp/issues/12
        if (button):
            button['state'] = state
        else:
            raise NameError("No such Button - Cannot change state of button in GUI")
            

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
        path = path_to_files + "/" + pomp_tagged_dir + "/"
        store_log(self.arr,path,filename)
        
        # Running Tagging Method
        start_time = time.time()
        print("Tagging Log: Start at " + str(start_time))
        tag_UI_w_POMP(filename)
        end_time = time.time()
        print("Tagging Log: Complete at " + str(end_time))

        self.master.quit()