import tkinter as tk

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.master = self.root
        self.master.title("My GUI")

        self.prompt = "Text"
        self.result = None

        self.create_widgets()

        

    def create_widgets(self):
        
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