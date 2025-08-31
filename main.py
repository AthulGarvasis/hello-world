import tkinter as tk
from tkinter import ttk

def handle_button_click(clicked_button_text):
    current_text = result_var.get()
    
    # Check for consecutive operators before updating the expression
    # This prevents 'Error' when an operator is pressed multiple times
    operators = ['+', '-', 'x', '÷', '%']
    if clicked_button_text in operators and current_text and current_text[-1] in operators:
        return
        
    if clicked_button_text == "=":
        try:
            expression = current_text.replace("÷", "/").replace("x", "*")
            result = eval(expression)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            result_var.set(str(result))
        except Exception:
            result_var.set("Error")
            
    elif clicked_button_text == "C":
        result_var.set("")
        
    elif clicked_button_text == "DEL":
        result_var.set(current_text[:-1])

    elif clicked_button_text == "%":
        try:
            current_number = float(current_text)
            result_var.set(str(current_number / 100))
        except ValueError:
            result_var.set("Error")
            
    elif clicked_button_text == "±":
        try:
            current_number = float(current_text)
            result_var.set(str(-current_number))
        except ValueError:
            result_var.set("Error")
            
    else:
        result_var.set(current_text + clicked_button_text)

def handle_keyboard_input(event):
    key = event.char
    # Mapping keys to button text
    if key.isdigit() or key in ['+', '-', '.', '%']:
        handle_button_click(key)
    elif key == '*':
        handle_button_click('x')
    elif key == '/':
        handle_button_click('÷')
    elif event.keysym == 'Return':
        handle_button_click('=')
    elif event.keysym == 'BackSpace':
        handle_button_click('DEL')
    elif event.keysym == 'c' or event.keysym == 'C':
        handle_button_click('C')

# Set up the main window
root = tk.Tk()
root.title("Calculator")
result_var = tk.StringVar()
result_entry = ttk.Entry(root, textvariable=result_var, font=("Helvetica", 24), justify="right")
result_entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

# Button layout
buttons = [
    ("C", 1, 0), ("DEL", 1, 1), ("%", 1, 2), ("÷", 1, 3),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("x", 2, 3),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
    ("±", 5, 0), ("0", 5, 1), (".", 5, 2), ("=", 5, 3)
]

style = ttk.Style()
style.theme_use('default')
style.configure("TButton", font=("Helvetica", 16), width=5, relief="flat", borderwidth=0)
style.configure("Operand.TButton", background="#f0f0f0")
style.configure("Operator.TButton", background="#f5f5f5")
style.configure("Equals.TButton", background="#007acc", foreground="white")

for button_info in buttons:
    button_text, row, col = button_info[:3]
    colspan = button_info[3] if len(button_info) > 3 else 1
    
    style_name = "Operand.TButton"
    if button_text in ['C', 'DEL', '%', '±']:
        style_name = "Operator.TButton"
    elif button_text in ['=', '+', '-', 'x', '÷']:
        style_name = "Equals.TButton" if button_text == '=' else "Operator.TButton"
    
    button = ttk.Button(root, text=button_text, command=lambda text=button_text: handle_button_click(text), style=style_name)
    button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)

# Make the grid cells expandable
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Window sizing and keyboard bindings
root.geometry("400x500")
root.resizable(False, False)
root.bind("<Key>", handle_keyboard_input)

root.mainloop()