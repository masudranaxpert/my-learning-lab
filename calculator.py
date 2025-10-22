from tkinter import *

root = Tk()
root.title("My Frist App")
root.geometry("320x400")

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
    
    
def text_get():
    result = eval(TextBox.get("1.0", END).strip())
    TextBox.delete("1.0", END)   
    TextBox.insert(END, result)
    
def delete_one():
    TextBox.delete("end-1c", END)
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
buttonFrame.columnconfigure(1, weight=1,pad=5)
buttonFrame.columnconfigure(2, weight=1)
buttonFrame.columnconfigure(3, weight=1)
buttonFrame.columnconfigure(4, weight=1)

btn17 = Button(buttonFrame, text="⌫", font=("Arial",18), command=delete_one)
btn17.grid(column=0, row=0, sticky=W+E)
btn18 = Button(buttonFrame, text="AC", font=("Arial",18), command=clear)
btn18.grid(column=1, row=0, sticky=W+E)


btn1 = Button(buttonFrame, text="1", font=("Arial",18), command=insert_1)
btn1.grid(column=0, row=1, sticky=W+E)
btn2 = Button(buttonFrame, text="2", font=("Arial",18), command=insert_2)
btn2.grid(column=1, row=1, sticky=W+E)
btn3 = Button(buttonFrame, text="3", font=("Arial",18), command=insert_3)
btn3.grid(column=2, row=1, sticky=W+E)
btn4 = Button(buttonFrame, text="+", font=("Arial",18), command=insert_addition)
btn4.grid(column=3, row=1, sticky=W+E)

btn5 = Button(buttonFrame, text="4", font=("Arial",18), command=insert_4)
btn5.grid(column=0, row=2, sticky=W+E)
btn6 = Button(buttonFrame, text="5", font=("Arial",18), command=insert_5)
btn6.grid(column=1, row=2, sticky=W+E)
btn7 = Button(buttonFrame, text="6", font=("Arial",18), command=insert_6)
btn7.grid(column=2, row=2, sticky=W+E)
btn8 = Button(buttonFrame, text="-", font=("Arial",18), command=insert_subtraction)
btn8.grid(column=3, row=2, sticky=W+E)

btn9 = Button(buttonFrame, text="7", font=("Arial",18), command=insert_7)
btn9.grid(column=0, row=3, sticky=W+E)
btn10 = Button(buttonFrame, text="8", font=("Arial",18), command=insert_8)
btn10.grid(column=1, row=3, sticky=W+E)
btn11 = Button(buttonFrame, text="9", font=("Arial",18), command=insert_9)
btn11.grid(column=2, row=3, sticky=W+E)
btn12 = Button(buttonFrame, text="*", font=("Arial",18), command=insert_Multiplication)
btn12.grid(column=3, row=3, sticky=W+E)

btn13 = Button(buttonFrame, text="0", font=("Arial",18), command=insert_0)
btn13.grid(column=0, row=4, sticky=W+E)
btn14 = Button(buttonFrame, text=".", font=("Arial",18), command=insert_dot)
btn14.grid(column=1, row=4, sticky=W+E)
btn15 = Button(buttonFrame, text="/", font=("Arial",18), command=insert_Division)
btn15.grid(column=2, row=4, sticky=W+E)
btn16 = Button(buttonFrame, text="=", font=("Arial",18), command=text_get)
btn16.grid(column=3, row=4, sticky=W+E)

buttonFrame.pack(fill="x", padx=20, pady=10)

root.mainloop()
