import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

DATA_FILE = "students.json"

# ---------- colors ----------
BG_COLOR = "lime green"
TEXT_COLOR = "purple"
BTN_COLOR = "white"
HOVER_COLOR = "lavender"

# ---------- helpers ----------
def grade(avg):
    if avg >= 75: return "A"
    if avg >= 65: return "B"
    if avg >= 50: return "C"
    if avg >= 40: return "D"
    return "F"

def load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                return json.load(f)
        except:
            messagebox.showwarning("Error", "Failed to load data.")
    return {}

def save(students):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(students, f, indent=2)
    except:
        messagebox.showerror("Error", "Failed to save data.")

students = load()

# ---------- hover effect ----------
def on_enter(e):
    e.widget["background"] = HOVER_COLOR

def on_leave(e):
    e.widget["background"] = BTN_COLOR

def styled_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        width=20,
        bg=BTN_COLOR,
        fg=TEXT_COLOR,
        activebackground=HOVER_COLOR
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.config(command=command)
    return btn

# ---------- core functions ----------
def add_student():
    sid = simpledialog.askstring("Input", "Enter ID:")
    if not sid:
        return
    if sid in students:
        messagebox.showerror("Error", "ID already exists")
        return

    name = simpledialog.askstring("Input", "Enter name:")
    prog = simpledialog.askstring("Input", "Enter program:")

    try:
        n = int(simpledialog.askstring("Input", "Number of subjects:"))
    except:
        messagebox.showerror("Error", "Invalid number")
        return

    subjects = {}
    for _ in range(n):
        sub = simpledialog.askstring("Input", "Subject:")
        try:
            mark = int(simpledialog.askstring("Input", f"Marks for {sub}:"))
            if 0 <= mark <= 100:
                subjects[sub] = mark
            else:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid marks")
            return

    students[sid] = {"name": name, "prog": prog, "subjects": subjects}
    save(students)
    messagebox.showinfo("Success", "Student added")

def view_all():
    if not students:
        messagebox.showinfo("Info", "No records")
        return

    text = ""
    for sid, s in students.items():
        avg = sum(s["subjects"].values()) / len(s["subjects"]) if s["subjects"] else 0
        text += f"{sid} | {s['name']} | {s['prog']} | Avg: {avg:.1f} ({grade(avg)})\n"

    show_text("All Students", text)

def report():
    sid = simpledialog.askstring("Input", "Enter ID:")
    s = students.get(sid)

    if not s:
        messagebox.showerror("Error", "Not found")
        return

    text = f"Name: {s['name']}\nProgram: {s['prog']}\n\nSubjects:\n"
    total = 0

    for sub, mark in s["subjects"].items():
        text += f"{sub}: {mark}\n"
        total += mark

    avg = total / len(s["subjects"]) if s["subjects"] else 0
    text += f"\nTotal: {total}\nAverage: {avg:.2f}\nGrade: {grade(avg)}"

    show_text("Report", text)

def update_student():
    sid = simpledialog.askstring("Input", "Enter ID:")
    s = students.get(sid)

    if not s:
        messagebox.showerror("Error", "Not found")
        return

    sub = simpledialog.askstring("Input", "Subject to update/add:")
    try:
        mark = int(simpledialog.askstring("Input", "New marks:"))
        if 0 <= mark <= 100:
            s["subjects"][sub] = mark
            save(students)
            messagebox.showinfo("Success", "Updated")
        else:
            raise ValueError
    except:
        messagebox.showerror("Error", "Invalid marks")

def delete_student():
    sid = simpledialog.askstring("Input", "Enter ID:")
    if sid not in students:
        messagebox.showerror("Error", "Not found")
        return

    if messagebox.askyesno("Confirm", "Delete this student?"):
        students.pop(sid)
        save(students)
        messagebox.showinfo("Success", "Deleted")

def search_student():
    q = simpledialog.askstring("Input", "Search ID or name:")
    if not q:
        return
    q = q.lower()

    result = ""
    for sid, s in students.items():
        if q in sid.lower() or q in s["name"].lower():
            result += f"{sid} | {s['name']}\n"

    if result:
        show_text("Search Results", result)
    else:
        messagebox.showinfo("Info", "No matches")

def stats():
    if not students:
        messagebox.showinfo("Info", "No data")
        return

    avgs = []
    for s in students.values():
        if s["subjects"]:
            avgs.append(sum(s["subjects"].values()) / len(s["subjects"]))

    if not avgs:
        messagebox.showinfo("Info", "No subject data")
        return

    text = f"Class Avg: {sum(avgs)/len(avgs):.2f}\n"
    text += f"Highest: {max(avgs):.2f}\nLowest: {min(avgs):.2f}\n"

    top = max(
        students.items(),
        key=lambda x: sum(x[1]["subjects"].values()) / len(x[1]["subjects"]) if x[1]["subjects"] else 0
    )

    text += f"Top Student: {top[1]['name']}"

    show_text("Statistics", text)

# ---------- helper window ----------
def show_text(title, content):
    win = tk.Toplevel(root)
    win.title(title)
    win.configure(bg=BG_COLOR)

    txt = tk.Text(win, width=60, height=20, fg=TEXT_COLOR)
    txt.pack()
    txt.insert(tk.END, content)
    txt.config(state="disabled")

# ---------- GUI ----------
root = tk.Tk()
root.title("Student Management System")
root.geometry("400x420")
root.configure(bg=BG_COLOR)

tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 16),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(pady=10)

styled_button(root, "Add Student", add_student).pack(pady=5)
styled_button(root, "View All", view_all).pack(pady=5)
styled_button(root, "Report", report).pack(pady=5)
styled_button(root, "Update", update_student).pack(pady=5)
styled_button(root, "Delete", delete_student).pack(pady=5)
styled_button(root, "Search", search_student).pack(pady=5)
styled_button(root, "Statistics", stats).pack(pady=5)
styled_button(root, "Exit", root.quit).pack(pady=10)

root.mainloop()