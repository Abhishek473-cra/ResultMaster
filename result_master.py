import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "results.json"

# ---------- Data Handling ----------

def load_data():
    if not os.path.exists(FILE_NAME):
        return {}
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Functions ----------

def add_result():
    try:
        roll = entry_roll.get().strip()
        name = entry_name.get().strip()
        marks = int(entry_marks.get())

        if roll == "" or name == "":
            messagebox.showerror("Error", "All fields are required")
            return

        data = load_data()

        if roll in data:
            messagebox.showerror("Error", "Result already exists")
            return

        result = "Pass" if marks >= 50 else "Fail"

        data[roll] = {
            "name": name,
            "marks": marks,
            "result": result
        }

        save_data(data)
        messagebox.showinfo("Success", "Result Added Successfully")
        clear_fields()

    except ValueError:
        messagebox.showerror("Error", "Marks must be a number")
    except:
        messagebox.showerror("Error", "Something went wrong")

def view_results():
    text_area.delete(1.0, tk.END)
    data = load_data()

    if not data:
        text_area.insert(tk.END, "No records found")
        return

    for roll, info in data.items():
        text_area.insert(
            tk.END,
            f"Roll: {roll} | Name: {info['name']} | Marks: {info['marks']} | Result: {info['result']}\n"
        )

def update_result():
    try:
        roll = entry_roll.get().strip()
        marks = int(entry_marks.get())

        data = load_data()

        if roll not in data:
            messagebox.showerror("Error", "Record not found")
            return

        data[roll]["marks"] = marks
        data[roll]["result"] = "Pass" if marks >= 33 else "Fail"

        save_data(data)
        messagebox.showinfo("Success", "Result Updated")
        clear_fields()
    except ValueError:
        messagebox.showerror("Error", "Marks must be a number")
    except:
        messagebox.showerror("Error", "Something went wrong")

def delete_result():
    roll = entry_roll.get().strip()
    data = load_data()

    if roll not in data:
        messagebox.showerror("Error", "Record not found")
        return

    del data[roll]
    save_data(data)
    messagebox.showinfo("Success", "Result Deleted")
    clear_fields()

def clear_fields():
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_marks.delete(0, tk.END)

def focus_to_name(event):
    entry_name.focus()

def focus_to_marks(event):
    entry_marks.focus()

def submit_form(event):
    add_result()
    entry_roll.focus()

# ---------- GUI ----------

root = tk.Tk()
root.title("Student Result Management System")
root.geometry("600x500")
root.resizable(False, False)

tk.Label(root, text="Student Result Management System", font=("Arial", 16, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Roll No").grid(row=0, column=0, padx=5, pady=5)
entry_roll = tk.Entry(frame)
entry_roll.grid(row=0, column=1)
entry_roll.bind("<Return>", focus_to_name)

tk.Label(frame, text="Name").grid(row=1, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=1, column=1)
entry_name.bind("<Return>", focus_to_marks)

tk.Label(frame, text="Marks").grid(row=2, column=0, padx=5, pady=5)
entry_marks = tk.Entry(frame)
entry_marks.grid(row=2, column=1)
entry_marks.bind("<Return>", submit_form)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", width=12, command=add_result).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="View", width=12, command=view_results).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Update", width=12, command=update_result).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Delete", width=12, command=delete_result).grid(row=0, column=3, padx=5)

text_area = tk.Text(root, height=12, width=70)
text_area.pack(pady=10)

root.mainloop()