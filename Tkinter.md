# 🎨 Tkinter GUI Programming Guide

A comprehensive guide to building graphical user interfaces with Python's Tkinter library.

---

## 📦 Step-01: Import
```python
from tkinter import *
```

We imported the tkinter module using `*`. This means we can use any function or class from tkinter without writing the module name.

> 💡 **Example:** You can just write `Button(...)`, `Label(...)`, etc., instead of `tkinter.Button(...)`

---

## 🪟 Step-02: Setting Main Application Window
```python
root = Tk()                      # Create Window
root.title("Feet to Meters")    # Set the window title
root.geometry("400x300")         # Set the window size
root.mainloop()                  # Keep the app running
```

`root.mainloop()` keeps the app running and handles events (like clicks). Without this, the window would close immediately, and you wouldn't see it.

---

## 📍 Step-03: Control Where to Place the Widget

### 🔹 `.pack()` Method

Arranges widgets one after another (top to bottom or left to right).

| Parameter | কাজ | উদাহরণ | নোট |
|-----------|-----|---------|------|
| `side=` | কোন দিক থেকে সাজাবে | `side=TOP` / `BOTTOM` / `LEFT` / `RIGHT` | Default: `TOP` |
| `fill=` | Widget কীভাবে space fill করবে | `fill=X` / `Y` / `BOTH` / `NONE` | X=horizontal, Y=vertical |
| `expand=` | Extra space নেবে কিনা | `expand=True` / `False` | `fill` এর সাথে ব্যবহার করতে হয় |
| `padx=` | Horizontal spacing (বাইরে) | `padx=10` বা `padx=(5, 10)` | tuple = (left, right) |
| `pady=` | Vertical spacing (বাইরে) | `pady=5` বা `pady=(5, 10)` | tuple = (top, bottom) |
| `ipadx=` | Internal horizontal padding | `ipadx=5` | Widget এর content এর জন্য |
| `ipady=` | Internal vertical padding | `ipady=5` | Widget এর content এর জন্য |
| `anchor=` | Widget এর alignment | `anchor=N` / `S` / `E` / `W` / `CENTER` | যখন extra space থাকে |

---

### 🔹 `.place()` Method

Sets a fixed position using x,y coordinates. Place widgets at an **exact position (x, y)** or in a **relative position**.
```python
widget.place(**options)
```

| Parameter | কাজ | উদাহরণ | নোট |
|-----------|-----|---------|------|
| `x=` | X coordinate (pixel) | `x=50` | বাম থেকে দূরত্ব |
| `y=` | Y coordinate (pixel) | `y=100` | উপর থেকে দূরত্ব |
| `relx=` | Relative X position (0.0 - 1.0) | `relx=0.5` | 0.5 = মাঝখানে (50%) |
| `rely=` | Relative Y position (0.0 - 1.0) | `rely=0.5` | 0.5 = মাঝখানে (50%) |
| `width=` | Widget এর width (pixel) | `width=200` | Fixed width |
| `height=` | Widget এর height (pixel) | `height=100` | Fixed height |
| `relwidth=` | Relative width (0.0 - 1.0) | `relwidth=0.5` | Parent এর 50% width |
| `relheight=` | Relative height (0.0 - 1.0) | `relheight=0.3` | Parent এর 30% height |
| `anchor=` | Widget এর anchor point | `anchor=CENTER` / `NW` / `SE` | Position এর reference point |
| `bordermode=` | Border এর বাইরে/ভিতরে | `bordermode=INSIDE` / `OUTSIDE` | Default: INSIDE |

---

### 🔹 `.grid()` Method

Arranges widgets in a grid using row and column. `padx`/`pady` adds space.

---

### 🔹 `.Frame()` Container

A Frame is a **container widget**. Any widgets you place inside a Frame will have that Frame as their parent.

**Frames are used to:**
- 📦 Group widgets: Keep related widgets together
- 🎯 Simplify layout: Divide a large GUI into smaller parts
```python
frame = Frame(parent, **options)
```

**Structure Example:**
```
root (Main Window)
└── my_frame (Frame)
    ├── button1
    └── button2
```

#### 📌 Notice:
- `my_frame = Frame(root, ...)` → Frame এর parent হলো `root`
- `Button(my_frame, ...)` → Button এর parent হলো `my_frame`

| Parameter | কাজ | উদাহরণ | নোট |
|-----------|-----|---------|------|
| `bg=` / `background=` | পেছনের রঙ | `bg="lightgray"` | Frame এর background color |
| `bd=` / `borderwidth=` | বর্ডারের পুরুত্ব | `bd=2` | Pixel এ |
| `relief=` | বর্ডার স্টাইল | `relief=RAISED` / `SUNKEN` / `FLAT` / `GROOVE` / `RIDGE` | Visual effect |
| `width=` | Frame এর width | `width=300` | Pixel এ |
| `height=` | Frame এর height | `height=200` | Pixel এ |
| `padx=` | Internal horizontal padding | `padx=10` | Frame এর ভিতরের space |
| `pady=` | Internal vertical padding | `pady=10` | Frame এর ভিতরের space |
| `cursor=` | Mouse cursor style | `cursor="hand2"` | যখন mouse frame এর উপর |
| `highlightbackground=` | Focus না থাকলে highlight color | `highlightbackground="blue"` | Border highlight |
| `highlightcolor=` | Focus থাকলে highlight color | `highlightcolor="red"` | Active state |
| `highlightthickness=` | Highlight border পুরুত্ব | `highlightthickness=2` | Pixel এ |

---

## 📝 Step-04: Content
```python
font=("Arial", 18)
bg="green"  # Background
pady=10     # 10 pixels of space above and below (padding)
padx=10     # 10 pixels of space left and right (padding)
```

### 🏷️ Label Widget
```python
label = Label(root, text="হ্যালো, Tkinter!")
```
Creates a Label Class. `root` is the parent (where it will be placed).
```python
label.pack()  # The pack() method places the widget in the window
```

The `config()` method is used to change widget properties.
```python
label.config(text="new text")
```

---

## ⌨️ Text Field Widgets

1. `Entry(root)` - Single line input
2. `Text(root)` - Multi-line input

### 🔹 Entry Widget

- Entry হলো **এক লাইনের টেক্সট ইনপুট**
- এতে প্রতিটি character এর অবস্থান **integer index** দিয়ে বোঝানো হয়:
  - `0` → শুরু
  - `END` → টেক্সটের একদম শেষের পরের জায়গা

---

### 🔹 Text Widget

- Text হলো **বহু লাইনের টেক্সট ইনপুট**
- এখানে index দুই ভাগে বিভক্ত: **`"line.column"`**
  - `"1.0"` → ১ম লাইনের ০তম পজিশন (অর্থাৎ একদম শুরু)
  - `"2.5"` → ২য় লাইনের ৫ নম্বর অক্ষর
  - `END` → টেক্সটের শেষ

💡 তাই `"1.0"` মানে `"line 1, character 0"` (অর্থাৎ টেক্সটের একদম শুরু)

---

### 🔹 Text Widget এ বিশেষ Index নোটেশন

Tkinter-এর Text widget সবসময় শেষে একটা অটো নিউলাইন (`\n`) রেখে দেয়।

তাই শেষের টেক্সট নিয়ে কাজ করতে এই বিশেষ index ব্যবহার করা হয়:

| Index | মানে |
|-------|------|
| `end-1c` | শেষের ১ অক্ষর আগের জায়গা (অর্থাৎ শেষের `\n` বাদ দিয়ে) |
| `end-2c` | শেষের ২ অক্ষর আগের জায়গা |

---

## 🔧 Entry Widget Methods

| Method | ব্যবহার | উদাহরণ |
|--------|----------|---------|
| `insert(index, text)` | নির্দিষ্ট অবস্থানে text যোগ করে | `entry.insert(END, "1")` |
| `delete(start, end=None)` | start থেকে end পর্যন্ত text মুছে দেয়। যদি end না দেও, start পজিশন মুছে হয় | `entry.delete(0, END)` → সব মুছে দেয় |
| `get()` | Entry-র সব text/string আনে | `value = entry.get()` |
| `select_range(start, end)` | নির্দিষ্ট range select করে | `entry.select_range(0, 5)` |
| `icursor(index)` | cursor-কে নির্দিষ্ট position এ রাখে | `entry.icursor(END)` |
| `index(index)` | নির্দিষ্ট position এর index number দেয় | `pos = entry.index(END)` |

---

## 🔧 Text Widget Methods

| Method | ব্যবহার | উদাহরণ |
|--------|----------|---------|
| `insert(index, text)` | নির্দিষ্ট index এ text যোগ করে | `text_widget.insert(END, "Hello")` |
| `delete(start, end=None)` | start থেকে end পর্যন্ত মুছে দেয় | `text_widget.delete("1.0", END)` → সব মুছে দেয় |
| `get(start, end)` | start থেকে end পর্যন্ত text আনে | `content = text_widget.get("1.0", END)` |
| `see(index)` | cursor/scroll কে নির্দিষ্ট index এ নিয়ে যায় | `text_widget.see(END)` |
| `mark_set(markName, index)` | mark বা cursor position set করে | `text_widget.mark_set("insert", END)` |
| `tag_add(tagName, start, end)` | text কে tag দিয়ে style করা | `text_widget.tag_add("highlight", "1.0", "1.5")` |
| `tag_config(tagName, **options)` | tag style define করে | `text_widget.tag_config("highlight", background="yellow")` |

---

### 📊 Index Comparison Table

| Widget | Index শুরু | Index শেষ | শেষের text মুছতে |
|--------|-----------|-----------|------------------|
| **Entry** | `0` | `END` | `entry.delete(entry.index(END)-1, END)` |
| **Text** | `"1.0"` | `END` বা `"end-1c"` | `text_widget.delete("end-2c", "end-1c")` |

---

## 📐 Grid Layout

Widgets are arranged in rows and columns using grid layout.

### 1️⃣ `grid()` Method - Widget Placement
```python
widget.grid(**options)
```

---

### 2️⃣ `columnconfigure()` - Column Setup
```python
root.columnconfigure(column_index, **options)
```

| Parameter | কাজ | উদাহরণ | নোট |
|-----------|-----|---------|------|
| `weight=` | Extra space কীভাবে distribute হবে | `weight=1` | বেশি weight = বেশি space |
| `minsize=` | Column এর minimum width (pixel) | `minsize=100` | এর চেয়ে ছোট হবে না |
| `pad=` | Column এর চারপাশে extra space | `pad=5` | সব widget এ প্রভাব ফেলে |
| `uniform=` | একই group এর column গুলো সমান width | `uniform="group1"` | Same name = same size |

### 3️⃣ `rowconfigure()` - Row Setup
```python
root.rowconfigure(row_index, **options)
```

| Parameter | কাজ | উদাহরণ | নোট |
|-----------|-----|---------|------|
| `weight=` | Extra space কীভাবে distribute হবে | `weight=1` | বেশি weight = বেশি space |
| `minsize=` | Row এর minimum height (pixel) | `minsize=50` | এর চেয়ে ছোট হবে না |
| `pad=` | Row এর চারপাশে extra space | `pad=5` | সব widget এ প্রভাব ফেলে |
| `uniform=` | একই group এর row গুলো সমান height | `uniform="group1"` | Same name = same size |

---

### 🧭 Sticky Directions
```
         N (North - উপর)
              |
W (West) -----+----- E (East)
    (বাম)     |     (ডান)
              |
         S (South - নিচ)
```

The `sticky` option in the grid layout tells you which side of its cell a widget should stick to.

- `N+S` will expand vertically (up-down)
- `W+E` will expand horizontally (left-right)
```python
# বাম দিকে align
label.grid(row=0, column=0, sticky=W)
```

---

## 🔘 Button Widget

The Button is the most important interactive widget.
```python
button = Button(parent, **options)
```

| Parameter | কাজ | উদাহরণ | নোট |
|-----------|-----|---------|------|
| `text=` | Button এর লেখা | `text="Click Me"` | Button এ যা দেখাবে |
| `command=` | **Click করলে কী হবে** | `command=my_function` | ⚠️ **বন্ধনী দেওয়া যাবে না!** |
| `bg=` / `background=` | পেছনের রঙ | `bg="blue"` | Button এর background |
| `fg=` / `foreground=` | টেক্সটের রঙ | `fg="white"` | Button এর text color |
| `font=` | ফন্ট স্টাইল | `font=("Arial", 14, "bold")` | (family, size, style) |
| `width=` | Button এর প্রশস্ততা | `width=20` | Characters এ (text এর জন্য) |
| `height=` | Button এর উচ্চতা | `height=2` | Lines এ (text এর জন্য) |
| `bd=` / `borderwidth=` | বর্ডারের পুরুত্ব | `bd=3` | Pixel এ |
| `relief=` | বর্ডার স্টাইল | `relief=RAISED` / `SUNKEN` / `FLAT` / `GROOVE` / `RIDGE` | 3D effect |
| `padx=` | Internal horizontal padding | `padx=10` | Text এর চারপাশে space |
| `pady=` | Internal vertical padding | `pady=5` | Text এর চারপাশে space |
| `state=` | Button সক্রিয় কিনা | `state=NORMAL` / `DISABLED` / `ACTIVE` | Disabled = click করা যাবে না |
| `cursor=` | Mouse cursor style | `cursor="hand2"` | যখন mouse button এর উপর |
| `activebackground=` | Click করার সময় background | `activebackground="lightblue"` | Active state color |
| `activeforeground=` | Click করার সময় foreground | `activeforeground="red"` | Active state text color |
| `image=` | Button এ image দেখানো | `image=my_photo` | PhotoImage object |
| `compound=` | Text ও image একসাথে | `compound=LEFT` / `RIGHT` / `TOP` / `BOTTOM` | Image এর position |
| `underline=` | কোন অক্ষর underline হবে | `underline=0` | 0 = প্রথম অক্ষর (keyboard shortcut) |
| `wraplength=` | Text wrap করার length | `wraplength=100` | Pixel এ, long text এর জন্য |
| `justify=` | Multi-line text alignment | `justify=LEFT` / `CENTER` / `RIGHT` | Text alignment |

---

## ⚡ `command=` Parameter

The `command` parameter is the most important. It defines what happens when the button is clicked.

### ✅ সঠিক উপায়:
```python
def my_function():
    print("Button clicked!")

# ✅ সঠিক - function এর নাম দিতে হবে (বন্ধনী ছাড়া)
button = Button(root, text="Click", command=my_function)
```

### ❌ ভুল উপায়:
```python
# ❌ ভুল - বন্ধনী দিলে function তৎক্ষণাৎ execute হয়ে যায়
button = Button(root, text="Click", command=my_function())
```

---

## 🔹 Arguments পাঠানোর উপায়

যদি function এ arguments পাঠাতে চাও, তাহলে **lambda** ব্যবহার করতে হবে।

### 💡 উদাহরণ 1: Simple Argument
```python
def greet(name):
    print(f"Hello, {name}!")

# lambda দিয়ে argument পাঠানো
button = Button(root, text="Greet", command=lambda: greet("John"))
```

### 💡 উদাহরণ 2: Multiple Arguments
```python
def calculate(a, b):
    result = a + b
    print(f"Result: {result}")

button = Button(root, text="Calculate", command=lambda: calculate(5, 3))
```

### 💡 উদাহরণ 3: Entry থেকে Value নিয়ে কাজ করা
```python
from tkinter import *

root = Tk()

entry = Entry(root)
entry.pack(pady=5)

def show_input():
    text = entry.get()
    print(f"You entered: {text}")

button = Button(root, text="Show", command=show_input)
button.pack(pady=5)

root.mainloop()
```

### 💡 উদাহরণ 4: Button থেকে Text পরিবর্তন
```python
from tkinter import *

root = Tk()

def change_text():
    button.config(text="Clicked!")

button = Button(root, text="Click Me", command=change_text)
button.pack(pady=10)

root.mainloop()
```

---

## 🎯 Button এর অন্যান্য Techniques

### 1️⃣ Button Disable/Enable করা
```python
def disable_button():
    button.config(state=DISABLED)

def enable_button():
    button.config(state=NORMAL)

button = Button(root, text="Click", command=disable_button)
button.pack()
```

### 2️⃣ Button এর Text পরিবর্তন
```python
count = 0

def increment():
    global count
    count += 1
    button.config(text=f"Count: {count}")

button = Button(root, text="Count: 0", command=increment)
button.pack()
```

### 3️⃣ Image Button
```python
from tkinter import *

root = Tk()

# Image load করা
photo = PhotoImage(file="icon.png")

# Image button
button = Button(root, image=photo, command=lambda: print("Image clicked!"))
button.pack()

# ⚠️ Image reference রাখতে হবে, নইলে garbage collect হয়ে যাবে
button.image = photo

root.mainloop()
```

### 4️⃣ Text + Image একসাথে
```python
photo = PhotoImage(file="icon.png")

button = Button(root, text="Save", image=photo, compound=LEFT, command=save_file)
button.pack()
button.image = photo
```

---


## 📄 License

This guide is open for educational purposes.

---

**Made with ❤️ for Python GUI learners**
