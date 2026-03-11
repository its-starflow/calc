import tkinter as tk

expression = ""

def press(num):
    global expression
    expression += str(num)
    equation.set(expression)

def equal():
    global expression
    try:
        result = str(eval(expression))
        equation.set(result)
        expression = result
    except:
        equation.set("error")
        expression = ""

def clear():
    global expression
    expression = ""
    equation.set("")

root = tk.Tk()
root.title("Calculator")
root.geometry("300x350")

equation = tk.StringVar()

display = tk.Entry(root, textvariable=equation, font=("Arial",20), justify="right")
display.pack(fill="both", ipadx=8, ipady=15)

frame = tk.Frame(root)
frame.pack()

buttons = [
("7",1,0),("8",1,1),("9",1,2),("/",1,3),
("4",2,0),("5",2,1),("6",2,2),("*",2,3),
("1",3,0),("2",3,1),("3",3,2),("-",3,3),
("0",4,0),(".",4,1),("+",4,2),("=",4,3)
]

for (text,row,col) in buttons:
    if text == "=":
        cmd = equal
    else:
        cmd = lambda x=text: press(x)

    tk.Button(frame, text=text, width=5, height=2, font=("Arial",14), command=cmd)\
        .grid(row=row, column=col)

tk.Button(root, text="Clear", command=clear).pack(fill="both")

root.mainloop()
