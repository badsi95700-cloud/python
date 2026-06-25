import tkinter as tk
import numpy as np

root = tk.Tk()
root.title("Advanced Scientific Calculator")
root.geometry("420x680")
root.resizable(False, False)
root.config(bg="#121212") # Deep dark background

expression = ""

# বাটন ক্লিক হ্যান্ডলার
def button_click(value):
    global expression
    if expression == "0":
        expression = value
    else:
        expression += value
    display_var.set(expression)

# চূড়ান্ত হিসাব নিকাশ
def calculate():
    global expression
    try:
        # টেক্সট এক্সপ্রেশনকে NumPy এর কোডে রূপান্তর
        calc_expression = expression.replace("sin", "np.sin(np.radians")
        calc_expression = calc_expression.replace("cos", "np.cos(np.radians")
        calc_expression = calc_expression.replace("tan", "np.tan(np.radians")
        calc_expression = calc_expression.replace("sqrt", "np.sqrt")
        calc_expression = calc_expression.replace("log", "np.log10")
        calc_expression = calc_expression.replace("ln", "np.log")
        calc_expression = calc_expression.replace("π", "np.pi")
        calc_expression = calc_expression.replace("e", "np.e")
        calc_expression = calc_expression.replace("Mod", "%")
        calc_expression = calc_expression.replace("Fact", "np.math.factorial")
        
        # ব্র্যাকেট ব্যালেন্স করা (sin/cos এর জন্য ডাবল ব্র্যাকেট সামলানো)
        for f in ["sin", "cos", "tan"]:
            if f in expression:
                open_brackets = calc_expression.count("(")
                close_brackets = calc_expression.count(")")
                if open_brackets > close_brackets:
                    calc_expression += ")" * (open_brackets - close_brackets)

        result = eval(calc_expression, {"np": np, "__builtins__": {}})
        
        if isinstance(result, float):
            result = round(result, 8)
            
        display_var.set(result)
        expression = str(result)
    except:
        display_var.set("Error")
        expression = ""

def clear():
    global expression
    expression = ""
    display_var.set("0")

def backspace():
    global expression
    # বড় ফাংশনগুলো একবারে কাটার জন্য
    if expression.endswith("sin(") or expression.endswith("cos(") or expression.endswith("tan("):
        expression = expression[:-4]
    elif expression.endswith("sqrt(") or expression.endswith("10^(") or expression.endswith("Fact("):
        expression = expression[:-5]
    elif expression.endswith("log(") or expression.endswith("ln("):
        expression = expression[:-4]
    elif expression.endswith("x²") or expression.endswith("x³"):
        expression = expression[:-2]
    else:
        expression = expression[:-1]
        
    if expression == "":
        expression = "0"
    display_var.set(expression)

def sci_function(func):
    global expression
    if expression == "0" or expression == "":
        if func == "x2": expression = "0"
        elif func == "x3": expression = "0"
        elif func == "pi": expression = "π"
        elif func == "e": expression = "e"
        elif func == "10x": expression = "10^("
        else: expression = func + "("
    else:
        if func == "x2": expression = f"({expression})**2"
        elif func == "x3": expression = f"({expression})**3"
        elif func == "10x": expression = f"10**({expression})"
        elif func == "pi": expression += "π"
        elif func == "e": expression += "e"
        else: expression += func + "("
    display_var.set(expression)

# --- ডিসপ্লে সেটআপ ---
display_var = tk.StringVar()
display_var.set("0")

# সুন্দর রাউন্ডেড লুকের জন্য ডিসপ্লে ফ্রেম
display_frame = tk.Frame(root, bg="#1a1a1a", bd=2, relief=tk.SOLID)
display_frame.pack(fill="x", padx=15, pady=20)

display = tk.Entry(
    display_frame,
    textvariable=display_var,
    font=("Helvetica", 32),
    bd=0,
    justify="right",
    bg="#1a1a1a",
    fg="#ffffff",
    insertbackground="white"
)
display.pack(fill="x", padx=15, pady=15)

# --- বাটন প্যানেল ---
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(fill="both", expand=True, padx=15, pady=5)

# আধুনিক বাটন লেআউট matrix
buttons = [
    ["sin", "cos", "tan", "C"],
    ["sqrt", "log", "ln", "⌫"],
    ["x²", "x³", "10ˣ", "Mod"],
    ["Fact", "π", "e", "/"],
    ["(", ")", "", "*"],  # একটি খালি জায়গা পরে মেইনটেইন করা হয়েছে
    ["7", "8", "9", "-"],
    ["4", "5", "6", "+"],
    ["1", "2", "3", "="],
    ["0", ".", "", ""]     # জিরো বাটন বড় করার জন্য স্পেসিং
]

# বাটন হোভার এফেক্ট (Mouse Hover)
def on_enter(e, hover_color):
    e.widget['background'] = hover_color

def on_leave(e, original_color):
    e.widget['background'] = original_color

# বাটন জেনারেটর লুপ
for row_idx, row in enumerate(buttons):
    for col_idx, btn_text in enumerate(row):
        if btn_text == "":
            continue
            
        # কালার স্কিম (Color Palette)
        if btn_text in ["sin", "cos", "tan", "sqrt", "log", "ln", "x²", "x³", "10ˣ", "Mod", "Fact", "π", "e"]:
            color = "#2d3250"       # সায়েন্টিফিক বাটন (Dark Blue-Grey)
            hover_color = "#424769"
        elif btn_text == "=":
            color = "#f9b17a"       # সমান বাটন (Accent Orange)
            hover_color = "#fcd0a1"
        elif btn_text in ["C", "⌫"]:
            color = "#ff6b6b"       # ডিলিট বাটন (Coral Red)
            hover_color = "#ff8787"
        elif btn_text in ["/", "*", "-", "+"]:
            color = "#676f9d"       # অপারেটর বাটন (Muted Purple)
            hover_color = "#868fbc"
        else:
            color = "#1e1e24"       # সাধারণ নাম্বার বাটন (Soft Charcoal)
            hover_color = "#2a2a35"

        # কমান্ড সেটআপ
        if btn_text == "sin": cmd = lambda: sci_function("sin")
        elif btn_text == "cos": cmd = lambda: sci_function("cos")
        elif btn_text == "tan": cmd = lambda: sci_function("tan")
        elif btn_text == "sqrt": cmd = lambda: sci_function("sqrt")
        elif btn_text == "log": cmd = lambda: sci_function("log")
        elif btn_text == "ln": cmd = lambda: sci_function("ln")
        elif btn_text == "x²": cmd = lambda: sci_function("x2")
        elif btn_text == "x³": cmd = lambda: sci_function("x3")
        elif btn_text == "10ˣ": cmd = lambda: sci_function("10x")
        elif btn_text == "Mod": cmd = lambda: button_click("Mod")
        elif btn_text == "Fact": cmd = lambda: sci_function("Fact")
        elif btn_text == "π": cmd = lambda: sci_function("pi")
        elif btn_text == "e": cmd = lambda: sci_function("e")
        elif btn_text == "=": cmd = calculate
        elif btn_text == "C": cmd = clear
        elif btn_text == "⌫": cmd = backspace
        else: cmd = lambda v=btn_text: button_click(v)

        # বাটন তৈরি
        btn = tk.Button(
            btn_frame,
            text=btn_text,
            font=("Helvetica", 14, "bold"),
            bg=color,
            fg="white",
            activebackground=hover_color,
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=cmd,
            bd=0
        )
        
        # বিশেষ বাটনের গ্রিড সাইজ অ্যাডজাস্টমেন্ট
        if btn_text == "0":
            btn.grid(row=row_idx, column=col_idx, columnspan=2, padx=5, pady=5, sticky="nsew")
        elif btn_text == ".":
            btn.grid(row=row_idx, column=2, padx=5, pady=5, sticky="nsew")
        elif btn_text == "=":
            btn.grid(row=row_idx-1, column=3, rowspan=2, padx=5, pady=5, sticky="nsew")
        elif btn_text in ["(", ")"]:
            btn.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew")
        elif row_idx == 4 and btn_text == "*":
            btn.grid(row=row_idx, column=3, padx=5, pady=5, sticky="nsew")
        else:
            btn.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew")

        # হোভার ইফেক্ট বাইন্ড করা
        btn.bind("<Enter>", lambda e, hc=hover_color: on_enter(e, hc))
        btn.bind("<Leave>", lambda e, oc=color: on_leave(e, oc))

# গ্রিড কনফিগারেশন
for i in range(9):
    btn_frame.rowconfigure(i, weight=1)
for j in range(4):
    btn_frame.columnconfigure(j, weight=1)

root.mainloop()
