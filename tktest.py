import tkinter as tk

class FruitDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Fruit Selection")
        
        label = tk.Label(self.top, text="Choose a fruit:")
        label.pack(pady=10)
        
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=10)
        
        apple_button = tk.Button(button_frame, text="Apples", 
                                command=self.choose_apple)
        apple_button.grid(row=0, column=0, padx=10)
        
        banana_button = tk.Button(button_frame, text="Banana", 
                                 command=self.choose_banana)
        banana_button.grid(row=0, column=1, padx=10)
        
        self.result = None
    
    def choose_apple(self):
        print("apple")
        self.result = "apple"
        self.top.destroy()
    
    def choose_banana(self):
        print("banana")
        self.result = "banana"
        self.top.destroy()

def show_fruit_dialog():
    dialog = FruitDialog(root)
    root.wait_window(dialog.top)
    print(f"Selected fruit: {dialog.result}")
    result_label.config(text=f"You selected: {dialog.result}")

# Create the main window
root = tk.Tk()
root.title("Dialog Box Example")
root.geometry("300x150")

# Button to open the dialog
open_button = tk.Button(root, text="Open Fruit Dialog", command=show_fruit_dialog)
open_button.pack(pady=20)

# Label to show the result
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
