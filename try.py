import tkinter as tk
from tkinter import messagebox, ttk
import json

FILE = "students.json"

# ===================== DATA =====================
def load_students():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_students(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ===================== SCREEN SWITCH =====================
def show_frame(frame):
    main_menu.pack_forget()
    add_frame.pack_forget()
    view_frame.pack_forget()
    edit_frame.pack_forget()
    student_frame.pack_forget()
    frame.pack(fill="both", expand=True)

# ===================== ADD STUDENT =====================
def add_student():
    root.geometry("700x500")
    show_frame(add_frame)

def setup_add():
    subjects = []

    tk.Label(add_frame, text="Add Student", bg="#4CAF50",
             fg="white", font=("Arial", 16, "bold")).pack(fill="x")

    form = tk.Frame(add_frame, bg="#eef3f7")
    form.pack(pady=10)

    tk.Label(form, text="Name", bg="#eef3f7").grid(row=0, column=0)
    name_entry = tk.Entry(form, width=25)
    name_entry.grid(row=0, column=1)

    tk.Label(form, text="ID", bg="#eef3f7").grid(row=1, column=0)
    id_entry = tk.Entry(form, width=25)
    id_entry.grid(row=1, column=1)

    tk.Label(form, text="Program  ", bg="#eef3f7").grid(row=2, column=0)
    course_entry = tk.Entry(form, width=25)
    course_entry.grid(row=2, column=1)

    tk.Label(add_frame, text="Courses",
             bg="#eef3f7", font=("Arial", 11, "bold")).pack(pady=(10, 2))

    subjects_frame = tk.Frame(add_frame, bg="#eef3f7")
    subjects_frame.pack()
    # HEADERS
    tk.Label(subjects_frame, text="Course", bg="#eef3f7", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
    tk.Label(subjects_frame, text="Grade", bg="#eef3f7", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
    tk.Label(subjects_frame, text="Units", bg="#eef3f7", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)

    def add_subject_row():
        row_index = len(subjects) + 1  

        sub_entry = tk.Entry(subjects_frame, width=15)
        sub_entry.grid(row=row_index, column=0, padx=5, pady=2)

        grade_entry = tk.Entry(subjects_frame, width=10)
        grade_entry.grid(row=row_index, column=1, padx=5)

        unit_entry = tk.Entry(subjects_frame, width=5)
        unit_entry.grid(row=row_index, column=2, padx=5)

        subjects.append((sub_entry, grade_entry, unit_entry))

    add_subject_row()

    def save_student():
        name = name_entry.get()
        sid = id_entry.get().strip()
        program = course_entry.get()

        if name == "" or sid == "":
            messagebox.showwarning("Error", "Name and ID required!")
            return

        data = load_students()

        for student in data:
            if str(student["id"]) == sid:
                messagebox.showerror("Duplicate ID", "Student ID already exists!")
                return

        subject_list = []
        for s, g, u in subjects:
            if s.get() and g.get() and u.get():
                subject_list.append({
                    "course": s.get(),
                    "grade": g.get(),
                    "units": u.get()
                })

        data.append({
            "name": name,
            "id": sid,
            "course": program,
            "subjects": subject_list
        })

        save_students(data)
        messagebox.showinfo("Saved", "Student saved!")

    tk.Button(add_frame, text="+ Add Course",
              bg="#4CAF50", fg="white",
              command=add_subject_row).pack(pady=5)

    btn_frame = tk.Frame(add_frame, bg="#eef3f7")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Back",
              bg="#bae8f3", fg="black",
            width=12,
            command=lambda: show_frame(main_menu)
            ).grid(row=0, column=0, padx=5)

    tk.Button(btn_frame, text="Save",
            bg="#bae8f3", fg="black",
            width=12,
            command=save_student
            ).grid(row=0, column=1, padx=5)
# ===================== VIEW STUDENTS =====================

def setup_view():
    global tree, detail_body

    style = ttk.Style()
    style.theme_use("clam") 

    style.configure("Treeview.Heading",
                    background="#84A7CA",
                    foreground="white",
                    font=("Arial", 11, "bold"))

    style.map("Treeview.Heading",
              background=[("active", "#1565C0")])

    style.configure("Treeview",
                    rowheight=28,
                    font=("Arial", 10))

    tk.Label(view_frame, text="View Students",
             bg="#1976D2", fg="white",
             font=("Arial", 16, "bold")).pack(fill="x")

    main_frame = tk.Frame(view_frame, bg="#eef3f7")
    main_frame.pack(fill="both", expand=True)

    columns = ("ID", "Name", "Program")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    tree.grid(row=0, column=0, padx=10, pady=10)

    # ===== RIGHT PANEL =====
    detail_frame = tk.Frame(
        main_frame,
        bg="#eef3f7",
        bd=2,
        relief="solid",
        highlightbackground="#aac9f7",
        highlightthickness=1
    )
    detail_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    canvas = tk.Canvas(detail_frame, bg="#eef3f7", highlightthickness=0)
    scrollbar = tk.Scrollbar(detail_frame, orient="vertical", command=canvas.yview)

    detail_body = tk.Frame(canvas, bg="#eef3f7")

    detail_body.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=detail_body, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ===== SHOW DETAILS =====
    def show_details(event):
        for w in detail_body.winfo_children():
            w.destroy()

        selected = tree.selection()
        if not selected:
            return

        sid = str(tree.item(selected[0], "values")[0])
        data = load_students()

        for s in data:
            if str(s["id"]) == sid:

                header = tk.Frame(detail_body, bg="#0d47a1")
                header.pack(fill="x")

                tk.Label(header, text="Student Details",
                         bg="#0d47a1", fg="white",
                         font=("Arial", 14, "bold")).pack(pady=10)

                info = tk.Frame(detail_body, bg="white", bd=1, relief="solid")
                info.pack(fill="x", padx=10, pady=10)

                tk.Label(info, text="Name:", bg="white", fg="gray").pack(anchor="w", padx=10)
                tk.Label(info, text=s["name"].upper(),
                         bg="white", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)

                tk.Label(info, text="Program:", bg="white", fg="gray").pack(anchor="w", padx=10, pady=(10, 0))
                tk.Label(info, text=s["course"],
                         bg="white", font=("Arial", 11)).pack(anchor="w", padx=10, pady=(0, 10))

                tk.Label(detail_body, text="COURSES",
                         bg="#eef3f7", fg="#0d47a1",
                         font=("Arial", 11, "bold")).pack(anchor="w", padx=12)

                table_frame = tk.Frame(detail_body, bg="white", bd=1, relief="solid")
                table_frame.pack(fill="both", padx=10, pady=5)

                cols = ("No.", "Course", "Grade", "Units")
                course_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=6)

                for col in cols:
                    course_tree.heading(col, text=col)
                    course_tree.column(col, anchor="center", width=90)

                course_tree.pack(fill="both", expand=True)

                total_units = 0
                for i, sub in enumerate(s["subjects"], start=1):
                    course_tree.insert("", "end",
                        values=(i, sub["course"], sub["grade"], sub["units"]))
                    total_units += float(sub["units"])

                total_frame = tk.Frame(detail_body, bg="#eef3f7", bd=1, relief="solid")
                total_frame.pack(fill="x", padx=10, pady=10)

                tk.Label(total_frame, text="Total Units:", bg="#eef3f7").pack(side="right", padx=5)
                tk.Label(total_frame, text=str(int(total_units)),
                         bg="#eef3f7", fg="#0d47a1",
                         font=("Arial", 11, "bold")).pack(side="right")

                break

    tree.bind("<<TreeviewSelect>>", show_details)

    # ===== BUTTONS =====
    btn_frame = tk.Frame(view_frame, bg="#eef3f7")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Delete", bg="#e53935",
              fg="white", width=10,
              command=delete_student).grid(row=0, column=0, padx=5)

    tk.Button(btn_frame, text="Refresh", bg="#1E88E5",
              fg="white", width=10,
              command=load_table).grid(row=0, column=1, padx=5)

    tk.Button(btn_frame, text="Back",
              width=10,
              command=lambda: show_frame(main_menu)
              ).grid(row=0, column=2, padx=5)
    
def view_students():
    root.geometry("900x550")
    show_frame(view_frame)
    load_table()

# ===================== EDIT STUDENT =====================
def edit_student_screen():
    root.geometry("700x500")
    show_frame(edit_frame)
    setup_edit()

def setup_edit():
    for widget in edit_frame.winfo_children():
        widget.destroy()

    tk.Label(edit_frame, text="Edit Student",
             bg="#FFC107", fg="black",
             font=("Arial", 16, "bold")).pack(fill="x")

    data = load_students()

    selected_student = {"data": None}
    subjects = []

    # ===== SELECT ID =====
    select_frame = tk.Frame(edit_frame, bg="#eef3f7")
    select_frame.pack(pady=10)

    tk.Label(select_frame, text="Select ID").grid(row=0, column=0)

    id_combo = ttk.Combobox(select_frame,
                            values=[s["id"] for s in data])
    id_combo.grid(row=0, column=1)

    # ===== FORM =====
    form = tk.Frame(edit_frame, bg="#eef3f7")
    form.pack()

    tk.Label(form, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(form)
    name_entry.grid(row=0, column=1)

    tk.Label(form, text="Program").grid(row=1, column=0)
    program_entry = tk.Entry(form)
    program_entry.grid(row=1, column=1)

    # ===== SUBJECTS =====
    subjects_frame = tk.Frame(edit_frame)
    subjects_frame.pack()

    def add_row(sub=None):
        row = len(subjects)

        c = tk.Entry(subjects_frame)
        g = tk.Entry(subjects_frame)
        u = tk.Entry(subjects_frame)

        c.grid(row=row, column=0)
        g.grid(row=row, column=1)
        u.grid(row=row, column=2)

        if sub:
            c.insert(0, sub["course"])
            g.insert(0, sub["grade"])
            u.insert(0, sub["units"])

        subjects.append((c, g, u))

    # ===== LOAD STUDENT =====
    def load_student():
        sid = id_combo.get()

        for s in data:
            if str(s["id"]) == sid:
                selected_student["data"] = s

                name_entry.delete(0, tk.END)
                name_entry.insert(0, s["name"])

                program_entry.delete(0, tk.END)
                program_entry.insert(0, s["course"])

                for w in subjects_frame.winfo_children():
                    w.destroy()
                subjects.clear()

                for sub in s["subjects"]:
                    add_row(sub)

    tk.Button(select_frame, text="Load",
              command=load_student).grid(row=0, column=2)

    tk.Button(edit_frame, text="Add Course",
              command=lambda: add_row()).pack()

    # ===== SAVE CHANGES (FIXED) =====
    def save_changes():
        if not selected_student["data"]:
            messagebox.showwarning("Error", "No student loaded!")
            return
        sid = selected_student["data"]["id"]
        updated_subjects = []
        for s, g, u in subjects:
            if s.get():
                updated_subjects.append({
                    "course": s.get(),
                    "grade": g.get(),
                    "units": u.get()
                })
        data = load_students()
        for student in data:
            if student["id"] == sid:
                student["name"] = name_entry.get()
                student["course"] = program_entry.get()
                student["subjects"] = updated_subjects

        save_students(data)
        messagebox.showinfo("Success", "Student updated!")

    # ===== BUTTONS =====
    tk.Button(edit_frame, text="Save Changes",
              bg="#00acc1", fg="white",
              command=save_changes).pack(pady=10)

    tk.Button(edit_frame, text="Back",
              command=lambda: show_frame(main_menu)).pack()

# ===================== TABLE =====================
def load_table():
    tree.delete(*tree.get_children())
    for s in load_students():
        tree.insert("", "end", values=(s["id"], s["name"], s["course"]))

def search_students_table_from_main(keyword):
    keyword = keyword.lower()

    student_tree.delete(*student_tree.get_children())

    for s in load_students():
        if (keyword in s["name"].lower() or
            keyword in str(s["id"]) or
            keyword in s["course"].lower()):

            student_tree.insert("", "end",
                                values=(s["id"], s["name"], s["course"]))

# ===================== DELETE =====================
def delete_student():
    selected = tree.selection()
    if not selected:
        return
    sid = tree.item(selected[0])["values"][0]
    data = [s for s in load_students() if s["id"] != sid]
    save_students(data)
    load_table()

# ===================== MAIN =====================
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x500")
root.configure(bg="#eef3f7")

main_menu = tk.Frame(root, bg="#eef3f7")
main_menu.pack(fill="both", expand=True)

# ===== HEADER =====
header = tk.Frame(main_menu, bg="#8fb7c7", height=80)
header.pack(fill="x")

tk.Label(header, text="Main Menu",
         bg="#8fb7c7", fg="black",
         font=("Arial", 28, "bold")).pack(pady=15)

# ===== BUTTON SECTION =====
btn_frame = tk.Frame(main_menu, bg="#eef3f7")
btn_frame.pack(pady=30)

btn_style = {
    "width": 20,
    "height": 2,
    "font": ("Arial", 14, "bold"),
    "bd": 2
}

tk.Button(btn_frame, text="Add Student",
          bg="#4CAF50", fg="white",
          command=add_student, **btn_style).pack(pady=10)

tk.Button(btn_frame, text="View Students",
          bg="#1E88E5", fg="white",
          command=view_students, **btn_style).pack(pady=10)

tk.Button(btn_frame, text="Edit Student",
          bg="#e0e0e0", fg="black",
          command=edit_student_screen, **btn_style).pack(pady=10)

# ===== SEARCH SECTION =====
search_frame = tk.Frame(main_menu, bg="#eef3f7")
search_frame.pack(pady=20)

tk.Label(search_frame, text="Search by Name or ID",
         bg="#eef3f7", font=("Arial", 10)).grid(row=0, column=0, columnspan=2, pady=5)

search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=1, column=0, padx=5)

def search_student():
    keyword = search_entry.get().lower()
    data = load_students()

    results = [s for s in data if keyword in s["name"].lower() or keyword in str(s["id"])]

    if not results:
        messagebox.showinfo("Search", "No student found.")
        return

def search_student():
    keyword = search_entry.get().strip()

    if keyword == "":
        messagebox.showwarning("Search", "Enter name or ID")
        return
    open_student_list()
    search_students_table_from_main(keyword)

tk.Button(search_frame, text="Search",
          bg="#00acc1", fg="white",
          width=12,
          command=search_student).grid(row=1, column=1, padx=5)

add_frame = tk.Frame(root, bg="#eef3f7")
view_frame = tk.Frame(root, bg="#eef3f7")
edit_frame = tk.Frame(root, bg="#eef3f7")

# ===================== STUDENT LIST UI =====================
def open_student_list():
    root.geometry("700x500")
    show_frame(student_frame)

def setup_student_list():
    global student_frame, student_tree, student_search

    student_frame = tk.Frame(root, bg="#eef3f7")

    # HEADER
    tk.Label(student_frame,
             text="Student List",
             bg="#1976D2",
             fg="white",
             font=("Arial", 18, "bold"),
             pady=10).pack(fill="x")

    # SEARCH
    search_frame = tk.Frame(student_frame, bg="#eef3f7")
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search:",
             bg="#eef3f7",
             font=("Arial", 11)).pack(side="left", padx=5)

    student_search = tk.Entry(search_frame, width=40,
                              font=("Arial", 10),
                              bd=2, relief="solid")
    student_search.pack(side="left", padx=5)

    tk.Button(search_frame, text="Search",
              bg="#00ACC1", fg="white",
              command=search_students_table).pack(side="left", padx=5)

    # TABLE
    table_frame = tk.Frame(student_frame)
    table_frame.pack(pady=10)

    columns = ("ID", "Name", "Program")
    student_tree = ttk.Treeview(table_frame,
                                columns=columns,
                                show="headings",
                                height=1)

    for col in columns:
        student_tree.heading(col, text=col)
        student_tree.column(col, anchor="center", width=180)

    student_tree.pack()

    # BACK BUTTON
    tk.Button(student_frame, text="Back",
          width=12,
          command=lambda: show_frame(main_menu)
          ).pack(pady=10)

def search_students_table():
    keyword = student_search.get().strip().lower()

    student_tree.delete(*student_tree.get_children())

    if keyword == "":
        return

    for s in load_students():
        if (keyword in s["name"].lower() or
            keyword in str(s["id"]) or
            keyword in s["course"].lower()):

            student_tree.insert("", "end",
                                values=(s["id"], s["name"], s["course"]))

def open_student_list():
    root.geometry("700x500")
    show_frame(student_frame)

setup_add()
setup_view()
setup_student_list()

root.mainloop()