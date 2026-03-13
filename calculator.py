import tkinter as tk
import math
from functools import partial

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("480x600")
        self.root.resizable(False, False)

        self.expression = ""          

        self.result_var = tk.StringVar(value="0")
        self.memory = 0                

        self.mode = "deg"               

        self.full_expression = ""       

        self.root.configure(bg="#2b2b2b")
        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):

        top_frame = tk.Frame(self.root, bg="#2b2b2b")
        top_frame.pack(fill="x", padx=5, pady=(5,0))

        self.memory_label = tk.Label(top_frame, text="", font=("Arial", 10), 
                                     fg="#ffcc00", bg="#2b2b2b")
        self.memory_label.pack(side="left")

        self.mode_label = tk.Label(top_frame, text="DEG", font=("Arial", 10, "bold"),
                                   fg="#87ceeb", bg="#2b2b2b")
        self.mode_label.pack(side="right")

        display_frame = tk.Frame(self.root, bg="#2b2b2b")
        display_frame.pack(fill="both", padx=10, pady=5)

        self.history_display = tk.Entry(display_frame, font=("Arial", 12), 
                                        fg="#aaa", bg="#1e1e1e", bd=0, 
                                        justify="right", state="readonly")
        self.history_display.pack(fill="x", ipady=2)

        self.result_display = tk.Entry(display_frame, textvariable=self.result_var,
                                       font=("Arial", 24, "bold"), 
                                       fg="white", bg="#1e1e1e", bd=0,
                                       justify="right")
        self.result_display.pack(fill="x", ipady=10)

        buttons_frame = tk.Frame(self.root, bg="#2b2b2b")
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)

        button_data = [

            ("MC", 0, 0, 1, "memory", "mc"),
            ("MR", 0, 1, 1, "memory", "mr"),
            ("M+", 0, 2, 1, "memory", "m+"),
            ("M-", 0, 3, 1, "memory", "m-"),
            ("MS", 0, 4, 1, "memory", "ms"),
            ("%", 0, 5, 1, "op", "%"),
            ("CE", 0, 6, 1, "clear", "ce"),
            ("C", 0, 7, 1, "clear", "c"),
            ("⌫", 0, 8, 1, "clear", "backspace"),

            ("x²", 1, 0, 1, "func", "square"),
            ("1/x", 1, 1, 1, "func", "reciprocal"),
            ("√", 1, 2, 1, "func", "sqrt"),
            ("xʸ", 1, 3, 1, "op", "**"),
            ("sin", 1, 4, 1, "func", "sin"),
            ("cos", 1, 5, 1, "func", "cos"),
            ("tan", 1, 6, 1, "func", "tan"),
            ("π", 1, 7, 1, "const", "pi"),
            ("e", 1, 8, 1, "const", "e"),

            ("x³", 2, 0, 1, "func", "cube"),
            ("∛", 2, 1, 1, "func", "cbrt"),
            ("log", 2, 2, 1, "func", "log"),
            ("ln", 2, 3, 1, "func", "ln"),
            ("(", 2, 4, 1, "op", "("),
            (")", 2, 5, 1, "op", ")"),
            ("n!", 2, 6, 1, "func", "factorial"),
            ("Rad", 2, 7, 1, "mode", None),
            ("Deg", 2, 8, 1, "mode", None),

            ("7", 3, 0, 1, "num", "7"),
            ("8", 3, 1, 1, "num", "8"),
            ("9", 3, 2, 1, "num", "9"),
            ("÷", 3, 3, 1, "op", "/"),
            ("4", 3, 4, 1, "num", "4"),
            ("5", 3, 5, 1, "num", "5"),
            ("6", 3, 6, 1, "num", "6"),
            ("×", 3, 7, 1, "op", "*"),
            ("1", 3, 8, 1, "num", "1"),

            ("2", 4, 0, 1, "num", "2"),
            ("3", 4, 1, 1, "num", "3"),
            ("–", 4, 2, 1, "op", "-"),
            ("+", 4, 3, 1, "op", "+"),
            ("0", 4, 4, 2, "num", "0"),
            (".", 4, 6, 1, "num", "."),
            ("±", 4, 7, 1, "func", "neg"),
            ("=", 4, 8, 1, "eval", None),
        ]

        for (text, r, c, colspan, cmd_type, value) in button_data:
            btn = self.create_button(buttons_frame, text, cmd_type, value)
            btn.grid(row=r, column=c, columnspan=colspan, 
                     sticky="nsew", padx=2, pady=2)

        for i in range(9):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)

    def create_button(self, parent, text, cmd_type, value):

        colors = {
            "num": ("#4a4a4a", "white"),
            "op": ("#ff9500", "white"),
            "func": ("#3a3a3a", "white"),
            "const": ("#3a3a3a", "#87ceeb"),
            "memory": ("#5a5a5a", "#ffcc00"),
            "clear": ("#b22222", "white"),
            "eval": ("#ff9500", "white", 2),
            "mode": ("#2a6f97", "white"),
        }
        fg = colors.get(cmd_type, ("#333", "white"))[1]
        bg = colors.get(cmd_type, ("#333",))[0]
        if cmd_type == "eval":

            btn = tk.Button(parent, text=text, font=("Arial", 14, "bold"),
                            bg=bg, fg=fg, bd=0, height=2)
        else:
            btn = tk.Button(parent, text=text, font=("Arial", 12),
                            bg=bg, fg=fg, bd=0, height=2)

        if cmd_type == "num":
            btn.config(command=partial(self.add_number, value))
        elif cmd_type == "op":
            btn.config(command=partial(self.add_operator, value))
        elif cmd_type == "func":
            btn.config(command=partial(self.add_function, value))
        elif cmd_type == "const":
            btn.config(command=partial(self.add_constant, value))
        elif cmd_type == "memory":
            btn.config(command=partial(self.memory_operation, value))
        elif cmd_type == "clear":
            btn.config(command=partial(self.clear_operation, value))
        elif cmd_type == "mode":
            if text == "Deg":
                btn.config(command=self.set_deg_mode)
            else:
                btn.config(command=self.set_rad_mode)
        elif cmd_type == "eval":
            btn.config(command=self.evaluate)

        return btn

    def add_number(self, num):
        self.expression += str(num)
        self.update_display()

    def add_operator(self, op):

        if self.expression and self.expression[-1] in "+-*/%**":
            self.expression = self.expression[:-1]
        self.expression += op
        self.update_display()

    def add_function(self, func):

        if func == "square":
            self.expression += "**2"
        elif func == "cube":
            self.expression += "**3"
        elif func == "sqrt":
            self.expression += "math.sqrt("
        elif func == "cbrt":
            self.expression += "**(1/3)"
        elif func == "log":
            self.expression += "math.log10("
        elif func == "ln":
            self.expression += "math.log("
        elif func == "sin":
            self.expression += "math.sin("
        elif func == "cos":
            self.expression += "math.cos("
        elif func == "tan":
            self.expression += "math.tan("
        elif func == "factorial":
            self.expression += "math.factorial("
        elif func == "neg":
            if self.expression and self.expression[-1].isdigit():

                self.expression += "*(-1)"
            else:
                self.expression += "(-"
        else:
            self.expression += func + "("
        self.update_display()

    def add_constant(self, const):
        if const == "pi":
            self.expression += "math.pi"
        elif const == "e":
            self.expression += "math.e"
        self.update_display()

    def memory_operation(self, op):
        try:
            current_val = float(self.result_var.get())
        except:
            current_val = 0

        if op == "mc":
            self.memory = 0
        elif op == "mr":
            self.expression += str(self.memory)
        elif op == "m+":
            self.memory += current_val
        elif op == "m-":
            self.memory -= current_val
        elif op == "ms":
            self.memory = current_val

        self.update_memory_indicator()
        if op == "mr":
            self.update_display()

    def clear_operation(self, op):
        if op == "c":
            self.expression = ""
            self.result_var.set("0")
        elif op == "ce":
            self.expression = ""
        elif op == "backspace":
            self.expression = self.expression[:-1]
        self.update_display()

    def set_deg_mode(self):
        self.mode = "deg"
        self.mode_label.config(text="DEG")

    def set_rad_mode(self):
        self.mode = "rad"
        self.mode_label.config(text="RAD")

    def evaluate(self):
        if not self.expression:
            return
        try:

            expr = self.expression

            import re
            expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
            expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
            expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)

            namespace = {"math": math, "__builtins__": {}}

            if self.mode == "deg":

                expr = re.sub(r'math\.sin\(([^)]+)\)', 
                              r'math.sin(math.radians(\1))', expr)
                expr = re.sub(r'math\.cos\(([^)]+)\)', 
                              r'math.cos(math.radians(\1))', expr)
                expr = re.sub(r'math\.tan\(([^)]+)\)', 
                              r'math.tan(math.radians(\1))', expr)

            result = eval(expr, namespace)

            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.result_var.set(str(result))
            self.expression = str(result)   

            self.history_display.config(state="normal")
            self.history_display.delete(0, tk.END)
            self.history_display.insert(0, expr)
            self.history_display.config(state="readonly")
        except Exception as e:
            self.result_var.set("Error")
            self.expression = ""

    def update_display(self):
        if self.expression:
            self.result_var.set(self.expression)
        else:
            self.result_var.set("0")

    def update_memory_indicator(self):
        if self.memory != 0:
            self.memory_label.config(text="M")
        else:
            self.memory_label.config(text="")

    def bind_keys(self):
        self.root.bind("<Key>", self.key_press)
        self.root.bind("<Return>", lambda e: self.evaluate())
        self.root.bind("<BackSpace>", lambda e: self.clear_operation("backspace"))
        self.root.bind("<Escape>", lambda e: self.clear_operation("c"))

    def key_press(self, event):
        key = event.char
        if key.isdigit() or key == '.':
            self.add_number(key)
        elif key in '+-*/%':
            self.add_operator(key)
        elif key == '(' or key == ')':
            self.add_operator(key)
        elif key == '=':
            self.evaluate()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
