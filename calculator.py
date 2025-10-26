from tkinter import *
from py_expression_eval import Parser

parser = Parser( )

root = Tk()
root.title("My Frist App")
root.geometry("350x400")

#Function
def insert_1():
    TextBox.insert(END,'1')
def insert_2():
    TextBox.insert(END,'2')
def insert_3():
    TextBox.insert(END,'3')
def insert_4():
    TextBox.insert(END,'4')
def insert_5():
    TextBox.insert(END,'5')
def insert_6():
    TextBox.insert(END,'6')
def insert_7():
    TextBox.insert(END,'7')
def insert_8():
    TextBox.insert(END,'8')
def insert_9():
    TextBox.insert(END,'9')
def insert_0():
    TextBox.insert(END,'0')
def insert_dot():
    TextBox.insert(END,'.')
def insert_addition():
    TextBox.insert(END,'+')
def insert_subtraction():
    TextBox.insert(END,'-')
def insert_Multiplication():
    TextBox.insert(END,'*')
def insert_Division():
    TextBox.insert(END,'/')
def insert_power():
    TextBox.insert(END,'^')
def insert_modulo():
    TextBox.insert(END,'%')
def insert_pi():
    TextBox.insert(END,'PI')
def insert_sin():
    TextBox.insert(END,'sin(')
def insert_cos():
    TextBox.insert(END,'cos(')
def insert_tan():
    TextBox.insert(END,'tan(')
def insert_asin():
    TextBox.insert(END,'asin(')
def insert_acos():
    TextBox.insert(END,'acos(')
def insert_atan():
    TextBox.insert(END,'atan(')
def insert_log():
    TextBox.insert(END,'log(')
    
    
def text_get():
    # result = eval(TextBox.get("1.0", END).strip())
    result = parser.parse(f'{TextBox.get("1.0", END).strip()}').evaluate({})
    TextBox.delete("1.0", END)   
    TextBox.insert(END, result)
    
def delete_one():
    TextBox.delete("end-2c", END)
def clear():
    TextBox.delete("1.0", END)

#Design
label = Label(root, text="Calculator", font=("Arial",18), bg="green")
label.pack()
TextBox = Text(root,height=2,font=("Arial",18), padx=10, pady=10)
TextBox.pack(padx=20,pady=10)


#Button
buttonFrame = Frame(root, height=50)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.columnconfigure(2, weight=2)
buttonFrame.columnconfigure(3, weight=1)
buttonFrame.columnconfigure(4, weight=1)
# buttonFrame.columnconfigure(5, weight=1)

btn17 = Button(buttonFrame, text="⌫", font=("Arial",18), height=1, command=delete_one)
btn17.grid(column=0, row=0, sticky=W+E)
btn18 = Button(buttonFrame, text="AC", font=("Arial",18), command=clear)
btn18.grid(column=1, row=0, sticky=W+E)
btn19 = Button(buttonFrame, text="^", font=("Arial",18), command=insert_power)
btn19.grid(column=2, row=0, sticky=W+E)
btn20 = Button(buttonFrame, text="%", font=("Arial",18), command=insert_modulo)
btn20.grid(column=3, row=0, sticky=W+E)
btn21 = Button(buttonFrame, text="π", font=("Arial",18), command=insert_pi)
btn21.grid(column=4, row=0, sticky=W+E)

btn1 = Button(buttonFrame, text="1", font=("Arial",18), command=insert_1)
btn1.grid(column=0, row=1, sticky=W+E)
btn2 = Button(buttonFrame, text="2", font=("Arial",18), command=insert_2)
btn2.grid(column=1, row=1, sticky=W+E)
btn3 = Button(buttonFrame, text="3", font=("Arial",18), command=insert_3)
btn3.grid(column=2, row=1, sticky=W+E)
btn4 = Button(buttonFrame, text="+", font=("Arial",18), command=insert_addition)
btn4.grid(column=3, row=1, sticky=W+E)
btn22 = Button(buttonFrame, text="sin", font=("Arial",18), command=insert_sin)
btn22.grid(column=4, row=1, sticky=W+E)

btn5 = Button(buttonFrame, text="4", font=("Arial",18), command=insert_4)
btn5.grid(column=0, row=2, sticky=W+E)
btn6 = Button(buttonFrame, text="5", font=("Arial",18), command=insert_5)
btn6.grid(column=1, row=2, sticky=W+E)
btn7 = Button(buttonFrame, text="6", font=("Arial",18), command=insert_6)
btn7.grid(column=2, row=2, sticky=W+E)
btn8 = Button(buttonFrame, text="-", font=("Arial",18), command=insert_subtraction)
btn8.grid(column=3, row=2, sticky=W+E)
btn23 = Button(buttonFrame, text="cos", font=("Arial",18), command=insert_cos)
btn23.grid(column=4, row=2, sticky=W+E)

btn9 = Button(buttonFrame, text="7", font=("Arial",18), command=insert_7)
btn9.grid(column=0, row=3, sticky=W+E)
btn10 = Button(buttonFrame, text="8", font=("Arial",18), command=insert_8)
btn10.grid(column=1, row=3, sticky=W+E)
btn11 = Button(buttonFrame, text="9", font=("Arial",18), command=insert_9)
btn11.grid(column=2, row=3, sticky=W+E)
btn12 = Button(buttonFrame, text="*", font=("Arial",18), command=insert_Multiplication)
btn12.grid(column=3, row=3, sticky=W+E)
btn24 = Button(buttonFrame, text="tan", font=("Arial",18), command=insert_tan)
btn24.grid(column=4, row=3, sticky=W+E)

btn13 = Button(buttonFrame, text="0", font=("Arial",18), command=insert_0)
btn13.grid(column=0, row=4, sticky=W+E)
btn14 = Button(buttonFrame, text=".", font=("Arial",18), command=insert_dot)
btn14.grid(column=1, row=4, sticky=W+E)
btn15 = Button(buttonFrame, text="/", font=("Arial",18), command=insert_Division)
btn15.grid(column=2, row=4, sticky=W+E)
btn16 = Button(buttonFrame, text="=", font=("Arial",18), command=text_get)
btn16.grid(column=3, row=4, sticky=W+E)
btn25 = Button(buttonFrame, text="log", font=("Arial",18), command=insert_log)
btn25.grid(column=4, row=4, sticky=W+E)

# btn26 = Button(buttonFrame, text="asin", font=("Arial",18), command=insert_asin)
# btn26.grid(column=0, row=5, sticky=W+E)
# btn27 = Button(buttonFrame, text="acos", font=("Arial",18), command=insert_acos)
# btn27.grid(column=1, row=5, sticky=W+E)
# btn28 = Button(buttonFrame, text="atan", font=("Arial",18), command=insert_atan)
# btn28.grid(column=2, row=5, sticky=W+E)

buttonFrame.pack(fill='x', padx=20, pady=10)

root.mainloop()
