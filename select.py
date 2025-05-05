import tkinter as tk

def select():
    # Variable to store the selected choice
    result = [None]  # Using a list to store by reference
    
    # Create the main window
    choice_select = tk.Tk()
    choice_select.title("Selection")
    choice_select.geometry("300x150")
    
    # Center the window on the screen
    # First, update the window to make sure we have the correct dimensions
    choice_select.update_idletasks()
    
    # Calculate position x and y coordinates
    width = choice_select.winfo_width()
    height = choice_select.winfo_height()
    screen_width = choice_select.winfo_screenwidth()
    screen_height = choice_select.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set the window position
    choice_select.geometry(f"{width}x{height}+{x}+{y}")

    # Function to handle button clicks
    def handle_choice(choice):
        result[0] = choice  # Store the choice
        choice_select.destroy()  # Close the window

    # Add a title label
    title_label = tk.Label(choice_select, text="Choose selection:", font=("Arial", 14))
    title_label.pack(pady=(10, 20))

    # Create frame to hold buttons
    button_frame = tk.Frame(choice_select)
    button_frame.pack()

    # Create two buttons with lambda to pass arguments to the handler
    FILE_button = tk.Button(
        button_frame, 
        text="selected FILE", 
        command=lambda: handle_choice("single"), 
        width=12
    )
    FILE_button.grid(row=0, column=0, padx=10)

    FOLDER_button = tk.Button(
        button_frame, 
        text="ENTIRE FOLDER", 
        command=lambda: handle_choice("folder"), 
        width=12
    )
    FOLDER_button.grid(row=0, column=1, padx=10)

    # Start the main event loop
    choice_select.mainloop()
    
    # After mainloop exits (when window is destroyed), return the result
    return result[0]

# Call the function and store the result
a = select()
print(a)
