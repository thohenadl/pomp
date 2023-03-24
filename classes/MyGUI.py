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
        self.contextValue_state = False
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
        self.add_menu()
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
            contextAttributes = context_attributes_smartRPA + context_attributes_ActionLogger
            if self.hideNAN_state & self.contextValue_state:
                # If both marks are checked, show only context values that are not nan
                all_cols = self.arr.columns.tolist()
                matching_cols = [col for col in contextAttributes if col in all_cols]
                text.insert(tk.END, self.arr[matching_cols].iloc[self.currentLine].dropna())
            elif self.hideNAN_state and not self.contextValue_state:
                # Shows all values that are not nan, including not context values
                text.insert(tk.END, self.arr.iloc[self.currentLine].dropna())
            elif not self.hideNAN_state and self.contextValue_state:
                # Only shows context values, including nan context values
                all_cols = self.arr.columns.tolist()
                matching_cols = [col for col in contextAttributes if col in all_cols]
                text.insert(tk.END, self.arr[matching_cols].iloc[self.currentLine])
            else:
                text.insert(tk.END, self.arr.iloc[self.currentLine])
        else:
            text.insert(tk.END, "All rows in selcted file have been tagged.")
            # Solves issue #12 https://github.com/thohenadl/pomp/issues/12
            self.set_button_state(self.button_tag,"disabled")
        text.grid(column = 0, row = 0, columnspan = 3, sticky='nsew')

    def widget_action_dropdown(self):
        """
        Creates a dropdown widget that allows the user to select an action from a list of pre-defined options.
        
        Args:
            None
            
        Returns:
            None
        """
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
    
    def widget_action_buttons(self, filename: str):
        """
        This function does create 3 buttons to tag the presented entry in the GUI.
            1. Button: Tags the current line
            2. Button: Does store the file and tagges all other files
            3. Button: Does store the file and does not tag other files.

        Args:
            filename (str): Does take the filename as input

        This function does not return any value.
        """
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
            text    = "Finish and Tag Files", 
            command = lambda: self.finish_and_tag_files(filename,True),
            # style   = "AccentButton",
            )
        self.button_finish.grid(column = 2, row = 2, sticky='nsew')

        self.button_finish = ttk.Button(
            master  = self.master, 
            text    = "Finish (w/o Tagging Files)", 
            command = lambda: self.finish_and_tag_files(filename,False),
            # style   = "AccentButton",
            )
        self.button_finish.grid(column = 3, row = 2, sticky='nsew')


    def change_HideNAN_state(self):
        # Solves issue #14 - https://github.com/thohenadl/pomp/issues/14
        if self.hideNAN_state:
            self.hideNAN_state = False
        else:
            self.hideNAN_state = True

    def change_contextValues_state(self):
        # Solves issue #14 - https://github.com/thohenadl/pomp/issues/14
        if self.contextValue_state:
            self.contextValue_state = False
        else:
            self.contextValue_state = True

    def toggle_hide_nan(self):
        self.change_HideNAN_state()
        self.widget_current_line_text()

    def toggle_context_values(self):
        self.change_contextValues_state()
        self.widget_current_line_text()

    def add_menu(self):
        """
        Adds a menu to the GUI with several buttons, such as "File" and "Options".

        The "File" button has a dropdown menu with a single option to "Open File Selection",
        which triggers the `reopen_file_dropdown` function when clicked.

        The "Options" button has a dropdown menu with two options: "Hide NaN Values" and 
        "Context Values Only", both of which trigger the `toggle_hide_nan` and 
        `toggle_context_values` functions respectively when clicked.

        This function does not return any value.
        """
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        # Menu Buttons
        file_menu = tk.Menu(menu, tearoff = False)
        options = tk.Menu(menu, tearoff = False)
        # Adding file_menu
        menu.add_cascade(label = "File", menu = file_menu)
        file_menu.add_command(label = "Open File Selection", command=self.reopen_file_dropdown)
        # Adding Options Menu
        menu.add_cascade(label="Options", menu = options)
        options.add_checkbutton(label="Hide NaN Values", command=self.toggle_hide_nan)
        options.add_checkbutton(label="Context Values Only", command=self.toggle_context_values)
        
    def reopen_file_dropdown(self):
        """
        Function does take in the GUI, removes all GUI elements and opens
            the file selction process again
        
        Args:
            -
            
        Returns:
            -
        """
        self.clear_gui()
        self.create_file_dropdown()

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
            

    def run(self):
        self.master.mainloop()

    def print_input(self, action):
        print("Selected Action: ", action)
        if action in action_Dimensions:
            self.arr.loc[self.currentLine, "pomp_dim"] = action
        
        self.currentLine += 1

    def clear_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def finish_and_tag_files(self, filename: str, override: bool):
        """
        Finish and tag log files.

        This function takes in a filename and an override flag. It stores the log file, then runs a tagging method
        on the file if the override flag is True. The function will then print the start and end time of the tagging 
        process and quit the GUI.

        Args:
            filename (str): The name of the file to tag.
            override (bool): A flag indicating whether to override the existing file if it has already been tagged.

        Returns:
            None
        """
        path = path_to_files + "/" + pomp_tagged_dir + "/"
        store_log(self.arr,path,filename)
        
        # Running Tagging Method
        if override:
            start_time = time.time()
            print("Tagging Log: Start at " + str(start_time))
            tag_UI_w_POMP(filename)
            end_time = time.time()
            print("Tagging Log: Complete at " + str(end_time))
        
        self.show_popup()

    def show_popup(self):
        """
        Create a popup window to show that the process has been completed.

        Returns:
            None

        """
        popup = tk.Toplevel(self.root)
        popup.title("Process Completed")
        popup.geometry("200x100")
        
        label = tk.Label(popup, text="Done!")
        label.pack(padx=20, pady=20)
        
        button = tk.Button(popup, text="Close", command=self.master.destroy)
        button.pack(padx=20, pady=10)

        # Center popup window on current GUI
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (self.root.winfo_width() // 2) - (width // 2)
        y = (self.root.winfo_height() // 2) - (height // 2)
        popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))