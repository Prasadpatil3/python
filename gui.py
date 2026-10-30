"""Tkinter GUI interface for Student Record Management System with Dynamic Subject Management."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Optional, List

from student import Student
from subject import Subject
from storage import StudentStorageManager, SubjectStorageManager
from validator import (
    ValidationError,
    DuplicateIDError,
    StudentNotFoundError,
    DuplicateSubjectError,
    SubjectNotFoundError,
    validate_student_id,
    validate_name,
    validate_class_div,
    validate_mark,
    validate_subject_name,
    validate_max_marks,
)


class SubjectManagementDialog(tk.Toplevel):
    """Modal dialog for viewing, adding, editing, and deleting configured subjects."""

    def __init__(self, parent: tk.Tk, storage: StudentStorageManager, on_update_callback):
        super().__init__(parent)
        self.title("Manage Subjects | Curriculum Configuration")
        self.geometry("640x500")
        self.minsize(580, 440)
        self.configure(bg="#F1F5F9")
        self.transient(parent)
        self.grab_set()

        self.storage = storage
        self.on_update_callback = on_update_callback
        self.selected_subject_id: Optional[str] = None

        self._create_header()
        self._create_content()
        self.refresh_subject_table()

    def _create_header(self) -> None:
        """Create top title banner."""
        header_frame = tk.Frame(self, bg="#1E3A8A", height=60)
        header_frame.pack(fill="x", side="top")

        lbl_title = tk.Label(
            header_frame,
            text="📚 Dynamic Subject Management",
            font=("Segoe UI", 13, "bold"),
            bg="#1E3A8A",
            fg="#FFFFFF"
        )
        lbl_title.pack(side="left", padx=16, pady=10)

        lbl_sub = tk.Label(
            header_frame,
            text="Configure subjects & maximum marks",
            font=("Segoe UI", 9),
            bg="#1E3A8A",
            fg="#BFDBFE"
        )
        lbl_sub.pack(side="right", padx=16, pady=12)

    def _create_content(self) -> None:
        """Create subjects table and editing form."""
        main_body = tk.Frame(self, bg="#F1F5F9", padx=15, pady=12)
        main_body.pack(fill="both", expand=True)

        # 1. Subjects Treeview Table
        table_card = tk.Frame(main_body, bg="#FFFFFF", relief="solid", bd=1, padx=8, pady=8)
        table_card.pack(fill="both", expand=True, pady=(0, 10))

        lbl_tbl = tk.Label(
            table_card,
            text="Configured Subjects List",
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#1E3A8A"
        )
        lbl_tbl.pack(anchor="w", pady=(0, 6))

        columns = ("id", "name", "max_marks")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=6, selectmode="browse")

        self.tree.heading("id", text="Subject ID", anchor="center")
        self.tree.heading("name", text="Subject Name", anchor="w")
        self.tree.heading("max_marks", text="Max Marks", anchor="center")

        self.tree.column("id", width=90, anchor="center")
        self.tree.column("name", width=280, anchor="w")
        self.tree.column("max_marks", width=110, anchor="center")

        y_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")

        self.tree.bind("<ButtonRelease-1>", self.handle_subject_selection)

        # 2. Add / Edit Subject Form Card
        form_card = tk.Frame(main_body, bg="#FFFFFF", relief="solid", bd=1, padx=12, pady=10)
        form_card.pack(fill="x")

        self.var_sub_name = tk.StringVar()
        self.var_sub_max = tk.StringVar(value="100")
        self.lbl_selected_info = tk.Label(
            form_card,
            text="Add a new subject or select one above to edit/delete:",
            font=("Segoe UI", 9, "italic"),
            bg="#FFFFFF",
            fg="#64748B"
        )
        self.lbl_selected_info.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))

        # Subject Name
        tk.Label(form_card, text="Subject Name *", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=4
        )
        self.entry_sub_name = ttk.Entry(form_card, textvariable=self.var_sub_name, width=28, font=("Segoe UI", 9))
        self.entry_sub_name.grid(row=1, column=1, sticky="w", pady=4, padx=(0, 15))

        # Max Marks
        tk.Label(form_card, text="Max Marks *", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).grid(
            row=1, column=2, sticky="w", padx=(0, 8), pady=4
        )
        self.entry_sub_max = ttk.Entry(form_card, textvariable=self.var_sub_max, width=10, font=("Segoe UI", 9))
        self.entry_sub_max.grid(row=1, column=3, sticky="w", pady=4)

        # Action Buttons
        btn_box = tk.Frame(form_card, bg="#FFFFFF")
        btn_box.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(10, 0))

        self.btn_add = tk.Button(
            btn_box,
            text="➕ Add Subject",
            command=self.handle_add_subject,
            bg="#2563EB",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.btn_add.pack(side="left", padx=3)

        self.btn_edit = tk.Button(
            btn_box,
            text="✏️ Update Subject",
            command=self.handle_edit_subject,
            bg="#0D9488",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.btn_edit.pack(side="left", padx=3)

        self.btn_del = tk.Button(
            btn_box,
            text="🗑️ Delete Subject",
            command=self.handle_delete_subject,
            bg="#DC2626",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.btn_del.pack(side="left", padx=3)

        self.btn_clear = tk.Button(
            btn_box,
            text="🔄 Clear",
            command=self.clear_subject_form,
            bg="#64748B",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.btn_clear.pack(side="left", padx=3)

        self.btn_close = tk.Button(
            btn_box,
            text="Close",
            command=self.destroy,
            bg="#E2E8F0",
            fg="#1E293B",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2"
        )
        self.btn_close.pack(side="right", padx=3)

    def refresh_subject_table(self) -> None:
        """Populate subject list in treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        subjects = self.storage.subject_manager.get_all_subjects()
        for sub in subjects:
            max_disp = int(sub.max_marks) if sub.max_marks.is_integer() else sub.max_marks
            self.tree.insert("", "end", values=(sub.id, sub.name, max_disp))

    def handle_subject_selection(self, event=None) -> None:
        """Load selected subject into editing fields."""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        values = self.tree.item(selected_items[0], "values")
        if not values:
            return

        sub_id = str(values[0])
        subject = self.storage.subject_manager.get_subject(sub_id)
        if not subject:
            return

        self.selected_subject_id = subject.id
        self.var_sub_name.set(subject.name)
        max_disp = int(subject.max_marks) if subject.max_marks.is_integer() else subject.max_marks
        self.var_sub_max.set(str(max_disp))
        self.lbl_selected_info.config(
            text=f"Selected: '{subject.name}' (ID: {subject.id}) | Ready to edit or delete."
        )

    def handle_add_subject(self) -> None:
        """Add new subject after validation."""
        try:
            existing_names = [s.name for s in self.storage.subject_manager.get_all_subjects()]
            name = validate_subject_name(self.var_sub_name.get(), existing_names)
            max_marks = validate_max_marks(self.var_sub_max.get())

            new_id = self.storage.subject_manager.generate_subject_id()
            new_subject = Subject(subject_id=new_id, name=name, max_marks=max_marks)

            self.storage.subject_manager.add_subject(new_subject)
            # Recalculate existing students' percentage with the new total max marks
            self.storage.recalculate_all_students()

            self.refresh_subject_table()
            self.clear_subject_form()
            self.on_update_callback()

            messagebox.showinfo("Success", f"Subject '{name}' added successfully (ID: {new_id})!")
        except (ValidationError, DuplicateSubjectError) as err:
            messagebox.showerror("Validation Error", str(err))
        except Exception as err:
            messagebox.showerror("Error", f"Could not add subject: {err}")

    def handle_edit_subject(self) -> None:
        """Update selected subject details with conflict checking."""
        if not self.selected_subject_id:
            messagebox.showwarning("Selection Required", "Please select a subject from the table to edit.")
            return

        subject = self.storage.subject_manager.get_subject(self.selected_subject_id)
        if not subject:
            messagebox.showerror("Not Found", "Selected subject no longer exists.")
            return

        try:
            # Check name uniqueness excluding the current subject
            other_names = [
                s.name for s in self.storage.subject_manager.get_all_subjects()
                if s.id != self.selected_subject_id
            ]
            new_name = validate_subject_name(self.var_sub_name.get(), other_names)
            new_max_marks = validate_max_marks(self.var_sub_max.get())

            # Validate that new maximum marks is not lower than any student's existing marks
            if new_max_marks < subject.max_marks:
                conflict = self.storage.check_subject_max_marks_conflict(
                    self.selected_subject_id, new_max_marks
                )
                if conflict:
                    student, mark_val = conflict
                    messagebox.showerror(
                        "Conflict Detected",
                        f"Cannot reduce maximum marks to {new_max_marks}.\n\n"
                        f"Student '{student.name}' (ID: {student.student_id}) has a mark of "
                        f"{mark_val} in '{subject.name}'.\n\n"
                        f"Please update the student's mark first before lowering the subject's maximum marks."
                    )
                    return

            # Apply updates
            subject.name = new_name
            subject.max_marks = new_max_marks
            self.storage.subject_manager.update_subject(subject)

            # Recalculate all students with updated max marks
            self.storage.recalculate_all_students()

            self.refresh_subject_table()
            self.clear_subject_form()
            self.on_update_callback()

            messagebox.showinfo("Success", f"Subject '{new_name}' updated successfully!")
        except (ValidationError, DuplicateSubjectError) as err:
            messagebox.showerror("Validation Error", str(err))
        except Exception as err:
            messagebox.showerror("Error", f"Failed to update subject: {err}")

    def handle_delete_subject(self) -> None:
        """Delete selected subject after confirmation and warning about consequences."""
        if not self.selected_subject_id:
            messagebox.showwarning("Selection Required", "Please select a subject from the table to delete.")
            return

        subject = self.storage.subject_manager.get_subject(self.selected_subject_id)
        if not subject:
            messagebox.showerror("Not Found", "Selected subject not found.")
            return

        total_subjects = len(self.storage.subject_manager.get_all_subjects())
        extra_warning = ""
        if total_subjects <= 1:
            extra_warning = "\n\n⚠️ CAUTION: This is the ONLY subject currently configured! Deleting it will leave the system with zero subjects."

        confirm = messagebox.askyesno(
            "Confirm Subject Deletion",
            f"Are you sure you want to delete '{subject.name}' ({subject.id})?\n\n"
            f"Consequences:\n"
            f"• This subject will be permanently removed from all active curriculum lists.\n"
            f"• Existing student marks for this subject will be removed.\n"
            f"• All student total marks, percentages, and grades will be automatically recalculated.{extra_warning}\n\n"
            f"Do you want to proceed?"
        )
        if not confirm:
            return

        try:
            self.storage.subject_manager.delete_subject(self.selected_subject_id)
            self.storage.remove_subject_from_students(self.selected_subject_id)

            self.refresh_subject_table()
            self.clear_subject_form()
            self.on_update_callback()

            messagebox.showinfo("Deleted", f"Subject '{subject.name}' was successfully removed.")
        except Exception as err:
            messagebox.showerror("Error", f"Failed to delete subject: {err}")

    def clear_subject_form(self) -> None:
        """Clear form inputs and deselect."""
        self.selected_subject_id = None
        self.var_sub_name.set("")
        self.var_sub_max.set("100")
        self.lbl_selected_info.config(
            text="Add a new subject or select one above to edit/delete:"
        )
        self.entry_sub_name.focus_set()


class StudentManagementApp:
    """Main GUI application class with dynamic subject support."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Student Record Management System | TY CSE")
        self.root.geometry("1120x700")
        self.root.minsize(1000, 620)
        self.root.configure(bg="#F1F5F9")

        self.storage = StudentStorageManager()
        self.selected_student_id: Optional[str] = None
        self.subject_vars: Dict[str, tk.StringVar] = {}
        self.subject_dialog: Optional[SubjectManagementDialog] = None

        self._configure_styles()
        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        self.refresh_table()

    def _configure_styles(self) -> None:
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use("clam")

        bg_card = "#FFFFFF"
        style.configure("Card.TFrame", background=bg_card, relief="flat")
        style.configure("TLabel", background=bg_card, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"), foreground="#1E293B", background=bg_card)
        style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#64748B", background=bg_card)
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=6)
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            rowheight=26,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 9)
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#E2E8F0",
            foreground="#0F172A",
            padding=5
        )
        style.map("Treeview", background=[("selected", "#3B82F6")], foreground=[("selected", "#FFFFFF")])

    def _create_header(self) -> None:
        """Create top title banner."""
        header_frame = tk.Frame(self.root, bg="#1E3A8A", height=70)
        header_frame.pack(fill="x", side="top")

        title_label = tk.Label(
            header_frame,
            text="🎓 Student Record Management System",
            font=("Segoe UI", 16, "bold"),
            bg="#1E3A8A",
            fg="#FFFFFF"
        )
        title_label.pack(side="left", padx=20, pady=12)

        subtitle_label = tk.Label(
            header_frame,
            text="Course: 231CSEPCC304 (Advanced Python) | TY CSE",
            font=("Segoe UI", 10),
            bg="#1E3A8A",
            fg="#BFDBFE"
        )
        subtitle_label.pack(side="right", padx=20, pady=16)

    def _create_main_content(self) -> None:
        """Create left form and right table panels."""
        content = tk.Frame(self.root, bg="#F1F5F9")
        content.pack(fill="both", expand=True, padx=15, pady=12)

        self.left_frame = tk.Frame(content, bg="#FFFFFF", padx=16, pady=14, relief="solid", bd=1, width=320)
        self.left_frame.pack(side="left", fill="y", padx=(0, 10))
        self.left_frame.pack_propagate(False)

        self.right_frame = tk.Frame(content, bg="#F1F5F9")
        self.right_frame.pack(side="right", fill="both", expand=True)

        self._build_form_inputs()
        self._build_search_and_table()

    def _build_form_inputs(self) -> None:
        """Build input form fields and action buttons."""
        lbl_form_title = tk.Label(
            self.left_frame,
            text="Student Details Form",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#1E3A8A"
        )
        lbl_form_title.pack(anchor="w", pady=(0, 10))

        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_class = tk.StringVar()
        self.var_percentage = tk.StringVar(value="-- %")
        self.var_grade = tk.StringVar(value="--")

        # Static Student Details Grid
        basic_info_frame = tk.Frame(self.left_frame, bg="#FFFFFF")
        basic_info_frame.pack(fill="x", pady=(0, 6))
        basic_info_frame.columnconfigure(1, weight=1)

        # Student ID
        tk.Label(basic_info_frame, text="Student ID *", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).grid(
            row=0, column=0, sticky="w", pady=3
        )
        self.entry_id = ttk.Entry(basic_info_frame, textvariable=self.var_id, width=18, font=("Segoe UI", 9))
        self.entry_id.grid(row=0, column=1, sticky="ew", pady=3, padx=(8, 0))

        # Student Name
        tk.Label(basic_info_frame, text="Full Name *", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).grid(
            row=1, column=0, sticky="w", pady=3
        )
        self.entry_name = ttk.Entry(basic_info_frame, textvariable=self.var_name, width=18, font=("Segoe UI", 9))
        self.entry_name.grid(row=1, column=1, sticky="ew", pady=3, padx=(8, 0))

        # Class / Division
        tk.Label(basic_info_frame, text="Class / Div *", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).grid(
            row=2, column=0, sticky="w", pady=3
        )
        self.entry_class = ttk.Entry(basic_info_frame, textvariable=self.var_class, width=18, font=("Segoe UI", 9))
        self.entry_class.grid(row=2, column=1, sticky="ew", pady=3, padx=(8, 0))

        # Dynamic Marks Header with Manage Subjects button
        ttk.Separator(self.left_frame, orient="horizontal").pack(fill="x", pady=6)

        marks_header_frame = tk.Frame(self.left_frame, bg="#FFFFFF")
        marks_header_frame.pack(fill="x", pady=(0, 4))

        tk.Label(
            marks_header_frame,
            text="Subject Marks",
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#0F172A"
        ).pack(side="left")

        btn_quick_manage = tk.Button(
            marks_header_frame,
            text="⚙️ Manage",
            command=self.open_subject_manager,
            bg="#EFF6FF",
            fg="#1E40AF",
            font=("Segoe UI", 8, "bold"),
            relief="groove",
            cursor="hand2",
            padx=6,
            pady=1
        )
        btn_quick_manage.pack(side="right")

        # Scrollable Subject Marks Container
        self.marks_canvas_frame = tk.Frame(self.left_frame, bg="#FFFFFF")
        self.marks_canvas_frame.pack(fill="x", pady=(2, 6))

        self.marks_canvas = tk.Canvas(self.marks_canvas_frame, bg="#FFFFFF", highlightthickness=0, height=140)
        self.marks_scrollbar = ttk.Scrollbar(
            self.marks_canvas_frame, orient="vertical", command=self.marks_canvas.yview
        )
        self.marks_inner_frame = tk.Frame(self.marks_canvas, bg="#FFFFFF")

        self.marks_inner_window = self.marks_canvas.create_window(
            (0, 0), window=self.marks_inner_frame, anchor="nw"
        )

        def _on_inner_configure(event):
            self.marks_canvas.configure(scrollregion=self.marks_canvas.bbox("all"))

        def _on_canvas_configure(event):
            self.marks_canvas.itemconfig(self.marks_inner_window, width=event.width)

        self.marks_inner_frame.bind("<Configure>", _on_inner_configure)
        self.marks_canvas.bind("<Configure>", _on_canvas_configure)
        self.marks_canvas.configure(yscrollcommand=self.marks_scrollbar.set)

        self.marks_canvas.pack(side="left", fill="both", expand=True)
        self.marks_scrollbar.pack(side="right", fill="y")

        # Result Preview Card
        result_box = tk.Frame(self.left_frame, bg="#EFF6FF", bd=1, relief="groove", padx=8, pady=6)
        result_box.pack(fill="x", pady=(4, 6))

        tk.Label(result_box, text="Percentage:", bg="#EFF6FF", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
        self.lbl_pct_val = tk.Label(
            result_box, textvariable=self.var_percentage, bg="#EFF6FF", font=("Segoe UI", 10, "bold"), fg="#1E40AF"
        )
        self.lbl_pct_val.grid(row=0, column=1, sticky="w", padx=6)

        tk.Label(result_box, text="Grade:", bg="#EFF6FF", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.lbl_grade_val = tk.Label(
            result_box, textvariable=self.var_grade, bg="#EFF6FF", font=("Segoe UI", 10, "bold"), fg="#059669"
        )
        self.lbl_grade_val.grid(row=0, column=3, sticky="w", padx=6)

        btn_calc = tk.Button(
            self.left_frame,
            text="🧮 Preview % & Grade",
            command=self.handle_preview_calc,
            bg="#EEF2F6",
            fg="#1E293B",
            font=("Segoe UI", 8, "bold"),
            relief="groove",
            cursor="hand2"
        )
        btn_calc.pack(fill="x", pady=(0, 6))

        # Action Buttons
        btn_frame = tk.Frame(self.left_frame, bg="#FFFFFF")
        btn_frame.pack(fill="x", pady=(2, 0))
        btn_frame.columnconfigure((0, 1), weight=1)

        self.btn_add = tk.Button(
            btn_frame,
            text="➕ Add Student",
            command=self.handle_add_student,
            bg="#2563EB",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=5
        )
        self.btn_add.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

        self.btn_update = tk.Button(
            btn_frame,
            text="✏️ Update",
            command=self.handle_update_student,
            bg="#0D9488",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=5
        )
        self.btn_update.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        self.btn_delete = tk.Button(
            btn_frame,
            text="🗑️ Delete",
            command=self.handle_delete_student,
            bg="#DC2626",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=5
        )
        self.btn_delete.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

        self.btn_clear = tk.Button(
            btn_frame,
            text="🔄 Clear Form",
            command=self.clear_form,
            bg="#64748B",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=5
        )
        self.btn_clear.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        # Initial render of dynamic subject inputs
        self._render_subject_mark_inputs()

    def _render_subject_mark_inputs(self) -> None:
        """Dynamically build subject mark entry fields based on configured subjects."""
        # Clear existing widgets in the marks container
        for widget in self.marks_inner_frame.winfo_children():
            widget.destroy()

        self.subject_vars.clear()
        subjects = self.storage.subject_manager.get_all_subjects()

        if not subjects:
            lbl_none = tk.Label(
                self.marks_inner_frame,
                text="⚠️ No subjects configured!\nClick 'Manage Subjects' to add one.",
                bg="#FFFFFF",
                fg="#DC2626",
                font=("Segoe UI", 9, "italic"),
                justify="center",
                pady=15
            )
            lbl_none.pack(fill="x")
            return

        self.marks_inner_frame.columnconfigure(1, weight=1)

        for idx, sub in enumerate(subjects):
            var = tk.StringVar()
            self.subject_vars[sub.id] = var

            max_disp = int(sub.max_marks) if sub.max_marks.is_integer() else sub.max_marks
            lbl_text = f"{sub.name} (/{max_disp}):"

            lbl = tk.Label(
                self.marks_inner_frame,
                text=lbl_text,
                bg="#FFFFFF",
                font=("Segoe UI", 9),
                anchor="w"
            )
            lbl.grid(row=idx, column=0, sticky="w", pady=3, padx=(0, 4))

            entry = ttk.Entry(
                self.marks_inner_frame,
                textvariable=var,
                width=10,
                font=("Segoe UI", 9)
            )
            entry.grid(row=idx, column=1, sticky="ew", pady=3)

    def _build_search_and_table(self) -> None:
        """Build search controls, action shortcuts, and dynamic Treeview table."""
        search_card = tk.Frame(self.right_frame, bg="#FFFFFF", padx=10, pady=8, relief="solid", bd=1)
        search_card.pack(fill="x", pady=(0, 10))

        tk.Label(
            search_card,
            text="🔍 Search:",
            bg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            fg="#334155"
        ).pack(side="left", padx=(0, 6))

        self.var_search = tk.StringVar()
        self.entry_search = ttk.Entry(search_card, textvariable=self.var_search, width=18, font=("Segoe UI", 9))
        self.entry_search.pack(side="left", padx=4)
        self.entry_search.bind("<Return>", lambda event: self.handle_search())

        tk.Button(
            search_card,
            text="Search",
            command=self.handle_search,
            bg="#3B82F6",
            fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            padx=8,
            pady=2,
            cursor="hand2"
        ).pack(side="left", padx=2)

        tk.Button(
            search_card,
            text="Show All",
            command=self.handle_reset_search,
            bg="#E2E8F0",
            fg="#1E293B",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            padx=8,
            pady=2,
            cursor="hand2"
        ).pack(side="left", padx=2)

        # Prominent Manage Subjects Button
        tk.Button(
            search_card,
            text="📚 Manage Subjects",
            command=self.open_subject_manager,
            bg="#1E40AF",
            fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            padx=10,
            pady=2,
            cursor="hand2"
        ).pack(side="right", padx=4)

        tk.Button(
            search_card,
            text="📊 View Charts",
            command=self.show_charts,
            bg="#ECFDF5",
            fg="#047857",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            padx=8,
            pady=2,
            cursor="hand2"
        ).pack(side="right", padx=2)

        tk.Button(
            search_card,
            text="Top Performers (Sort %)",
            command=self.handle_sort_percentage,
            bg="#F3E8FF",
            fg="#6B21A8",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            padx=8,
            pady=2,
            cursor="hand2"
        ).pack(side="right", padx=2)

        table_card = tk.Frame(self.right_frame, bg="#FFFFFF", relief="solid", bd=1)
        table_card.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_card,
            show="headings",
            selectmode="browse"
        )

        self.y_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.x_scroll = ttk.Scrollbar(table_card, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.y_scroll.set, xscrollcommand=self.x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.y_scroll.grid(row=0, column=1, sticky="ns")
        self.x_scroll.grid(row=1, column=0, sticky="ew")

        table_card.rowconfigure(0, weight=1)
        table_card.columnconfigure(0, weight=1)

        self.tree.bind("<ButtonRelease-1>", self.handle_row_selection)

        self._setup_treeview_columns()

    def _setup_treeview_columns(self) -> None:
        """Dynamically configure Treeview columns and headings based on configured subjects."""
        subjects = self.storage.subject_manager.get_all_subjects()
        total_max = self.storage.subject_manager.get_total_max_marks()

        # Build column identifiers
        cols: List[str] = ["id", "name", "class"]
        for sub in subjects:
            cols.append(f"sub_{sub.id}")
        cols.extend(["total", "percentage", "grade"])

        self.tree["columns"] = tuple(cols)

        # Configure base headers
        self.tree.heading("id", text="Student ID", anchor="center")
        self.tree.column("id", width=80, anchor="center")

        self.tree.heading("name", text="Full Name", anchor="w")
        self.tree.column("name", width=140, anchor="w")

        self.tree.heading("class", text="Class / Div", anchor="center")
        self.tree.column("class", width=90, anchor="center")

        # Configure dynamic subject headers
        for sub in subjects:
            col_id = f"sub_{sub.id}"
            max_disp = int(sub.max_marks) if sub.max_marks.is_integer() else sub.max_marks
            header_text = f"{sub.name} (/{max_disp})"
            col_width = max(80, min(140, len(sub.name) * 9))
            self.tree.heading(col_id, text=header_text, anchor="center")
            self.tree.column(col_id, width=col_width, anchor="center")

        # Configure summary headers
        max_tot_disp = int(total_max) if total_max.is_integer() else total_max
        self.tree.heading("total", text=f"Total (/{max_tot_disp})", anchor="center")
        self.tree.column("total", width=95, anchor="center")

        self.tree.heading("percentage", text="Percentage", anchor="center")
        self.tree.column("percentage", width=85, anchor="center")

        self.tree.heading("grade", text="Grade", anchor="center")
        self.tree.column("grade", width=60, anchor="center")

    def _create_status_bar(self) -> None:
        """Create bottom status bar."""
        self.status_frame = tk.Frame(self.root, bg="#CBD5E1", height=24)
        self.status_frame.pack(fill="x", side="bottom")

        self.lbl_status_text = tk.Label(
            self.status_frame,
            text="Ready | Records loaded from storage",
            bg="#CBD5E1",
            font=("Segoe UI", 9),
            fg="#1E293B"
        )
        self.lbl_status_text.pack(side="left", padx=12)

        self.lbl_record_count = tk.Label(
            self.status_frame,
            text=f"Total Students: {self.storage.get_total_count()}",
            bg="#CBD5E1",
            font=("Segoe UI", 9, "bold"),
            fg="#1E293B"
        )
        self.lbl_record_count.pack(side="right", padx=15)

    def open_subject_manager(self) -> None:
        """Open the dynamic Subject Management modal dialog."""
        if self.subject_dialog and self.subject_dialog.winfo_exists():
            self.subject_dialog.lift()
            self.subject_dialog.focus_force()
            return

        self.subject_dialog = SubjectManagementDialog(
            parent=self.root,
            storage=self.storage,
            on_update_callback=self.on_subjects_updated
        )

    def on_subjects_updated(self) -> None:
        """
        Callback triggered whenever subjects are added, edited, or removed.
        Refreshes form inputs, Treeview table columns, student rows, and status bar.
        """
        self._render_subject_mark_inputs()
        self._setup_treeview_columns()
        self.refresh_table()
        self.set_status("Curriculum updated. Form and table refreshed.")

    def _extract_and_validate_inputs(self) -> tuple:
        """Extract and validate form inputs against configured subjects."""
        subjects = self.storage.subject_manager.get_all_subjects()
        if not subjects:
            raise ValidationError(
                "No subjects configured! Please add at least one subject via 'Manage Subjects'."
            )

        student_id = validate_student_id(self.var_id.get())
        name = validate_name(self.var_name.get())
        class_div = validate_class_div(self.var_class.get())

        marks_dict: Dict[str, float] = {}
        for sub in subjects:
            raw_val = self.subject_vars.get(sub.id, tk.StringVar()).get()
            validated_val = validate_mark(sub.name, raw_val, max_marks=sub.max_marks)
            marks_dict[sub.id] = validated_val

        return student_id, name, class_div, marks_dict

    def handle_preview_calc(self) -> None:
        """Calculate and display percentage and grade preview dynamically."""
        subjects = self.storage.subject_manager.get_all_subjects()
        if not subjects:
            messagebox.showwarning(
                "No Subjects",
                "No subjects configured. Please configure subjects via 'Manage Subjects' first."
            )
            return

        try:
            total_obtained = 0.0
            total_max = self.storage.subject_manager.get_total_max_marks()

            for sub in subjects:
                raw_val = self.subject_vars.get(sub.id, tk.StringVar()).get()
                val = validate_mark(sub.name, raw_val, max_marks=sub.max_marks)
                total_obtained += val

            pct = round((total_obtained / total_max) * 100.0, 2) if total_max > 0 else 0.0

            temp_student = Student(
                student_id="TEMP",
                name="Preview",
                class_div="TEMP",
                marks={},
                percentage=pct,
                grade=None,
                max_possible_marks=total_max
            )
            grade = temp_student.calculate_grade(pct)

            self.var_percentage.set(f"{pct}%")
            self.var_grade.set(grade)

            tot_disp = int(total_obtained) if total_obtained.is_integer() else round(total_obtained, 2)
            max_disp = int(total_max) if total_max.is_integer() else round(total_max, 2)
            self.set_status(f"Calculated: {tot_disp}/{max_disp} marks ({pct}%) | Grade: {grade}")
        except ValidationError as ve:
            messagebox.showwarning("Validation Warning", str(ve))

    def handle_add_student(self) -> None:
        """Add new student record."""
        subjects = self.storage.subject_manager.get_all_subjects()
        if not subjects:
            messagebox.showerror(
                "No Subjects",
                "Cannot add student: No subjects configured!\n"
                "Please add at least one subject via 'Manage Subjects' before adding students."
            )
            return

        try:
            student_id, name, class_div, marks = self._extract_and_validate_inputs()
            max_possible = self.storage.subject_manager.get_total_max_marks()
            new_student = Student(
                student_id=student_id,
                name=name,
                class_div=class_div,
                marks=marks,
                max_possible_marks=max_possible
            )
            self.storage.add_student(new_student)

            self.refresh_table()
            self.clear_form()
            self.set_status(f"Student '{name}' (ID: {student_id}) added successfully!")
            messagebox.showinfo("Success", f"Student '{name}' added successfully!")
        except (ValidationError, DuplicateIDError) as err:
            messagebox.showerror("Error", str(err))
        except Exception as err:
            messagebox.showerror("Unexpected Error", f"An error occurred: {err}")

    def handle_update_student(self) -> None:
        """Update selected student record."""
        if not self.selected_student_id:
            messagebox.showwarning("Selection Required", "Please select a student from the table first.")
            return

        subjects = self.storage.subject_manager.get_all_subjects()
        if not subjects:
            messagebox.showerror("No Subjects", "No subjects configured.")
            return

        try:
            student_id, name, class_div, marks = self._extract_and_validate_inputs()

            if student_id != self.selected_student_id:
                confirm = messagebox.askyesno(
                    "ID Change Confirmation",
                    f"Change ID from '{self.selected_student_id}' to '{student_id}'?"
                )
                if not confirm:
                    return
                self.storage.delete_student(self.selected_student_id)

            max_possible = self.storage.subject_manager.get_total_max_marks()
            updated_student = Student(
                student_id=student_id,
                name=name,
                class_div=class_div,
                marks=marks,
                max_possible_marks=max_possible
            )

            if student_id == self.selected_student_id:
                self.storage.update_student(updated_student)
            else:
                self.storage.add_student(updated_student)

            self.refresh_table()
            self.clear_form()
            self.set_status(f"Student ID '{student_id}' updated successfully!")
            messagebox.showinfo("Success", f"Record for '{name}' updated successfully!")
        except (ValidationError, StudentNotFoundError, DuplicateIDError) as err:
            messagebox.showerror("Error", str(err))
        except Exception as err:
            messagebox.showerror("Error", f"Failed to update record: {err}")

    def handle_delete_student(self) -> None:
        """Delete selected student record after confirmation."""
        target_id = self.var_id.get().strip().upper() or self.selected_student_id
        if not target_id:
            messagebox.showwarning("Selection Required", "Please select a student record to delete.")
            return

        student = self.storage.get_student(target_id)
        if not student:
            messagebox.showerror("Not Found", f"No student found with ID '{target_id}'.")
            return

        if messagebox.askyesno("Confirm Delete", f"Delete student '{student.name}' (ID: {student.student_id})?"):
            try:
                self.storage.delete_student(student.student_id)
                self.refresh_table()
                self.clear_form()
                self.set_status(f"Student '{student.name}' deleted.")
                messagebox.showinfo("Deleted", "Student record successfully deleted.")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to delete student: {err}")

    def handle_row_selection(self, event=None) -> None:
        """Populate form with selected row data, mapping marks to configured subjects."""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        values = self.tree.item(selected_items[0], "values")
        if not values:
            return

        student = self.storage.get_student(str(values[0]))
        if not student:
            return

        self.selected_student_id = student.student_id
        self.var_id.set(student.student_id)
        self.var_name.set(student.name)
        self.var_class.set(student.class_div)

        subjects = self.storage.subject_manager.get_all_subjects()
        for sub in subjects:
            val = student.marks.get(sub.id, student.marks.get(sub.name, ""))
            if val != "":
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                self.subject_vars[sub.id].set(str(val))
            else:
                self.subject_vars[sub.id].set("")

        self.var_percentage.set(f"{student.percentage}%")
        self.var_grade.set(student.grade)
        self.set_status(f"Selected: {student.name} (ID: {student.student_id})")

    def handle_search(self) -> None:
        """Search students by ID or name."""
        query = self.var_search.get().strip()
        matched = self.storage.search_students(query)
        self.populate_treeview(matched)
        self.set_status(f"Search for '{query}' found {len(matched)} record(s).")

    def handle_reset_search(self) -> None:
        """Reset search and show all students."""
        self.var_search.set("")
        self.refresh_table()
        self.set_status("Displaying all student records.")

    def handle_sort_percentage(self) -> None:
        """Sort students by percentage (descending)."""
        sorted_students = self.storage.sort_students(by="percentage", reverse=True)
        self.populate_treeview(sorted_students)
        self.set_status("Sorted students by Percentage (descending).")

    def show_charts(self) -> None:
        """Display student performance charts dynamically using Matplotlib."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            messagebox.showerror("Error", "Matplotlib is not installed. Run: pip install matplotlib")
            return

        students = self.storage.get_all_students()
        if not students:
            messagebox.showwarning("No Data", "Please add students first to display charts.")
            return

        subjects = self.storage.subject_manager.get_all_subjects()
        has_subjects = len(subjects) > 0

        # Create Matplotlib Figure with 2 or 3 Subplots
        if has_subjects:
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.8))
        else:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

        fig.canvas.manager.set_window_title("Student Analytics & Visualizations")

        # 1. Bar Chart Data: Names & Percentages
        names = [s.name.split()[0] for s in students]
        percentages = [s.percentage for s in students]

        bars = ax1.bar(names, percentages, color="#3B82F6", edgecolor="#1E3A8A")
        ax1.axhline(40, color="red", linestyle="--", linewidth=1, label="Pass Mark (40%)")
        ax1.set_ylim(0, 105)
        ax1.set_title("Student Percentage Comparison", fontsize=11, fontweight="bold")
        ax1.set_ylabel("Percentage (%)")
        ax1.legend(loc="upper right")
        ax1.grid(axis="y", linestyle=":", alpha=0.6)

        for bar in bars:
            height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1.5,
                f"{height:.1f}%",
                ha="center",
                va="bottom",
                fontsize=8
            )

        # 2. Pie Chart Data: Grade Distribution
        grades = [s.grade for s in students]
        unique_grades = sorted(set(grades))
        grade_counts = [grades.count(g) for g in unique_grades]
        colors = ["#10B981", "#3B82F6", "#F59E0B", "#8B5CF6", "#EF4444", "#6B7280"]

        ax2.pie(
            grade_counts,
            labels=unique_grades,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors[:len(unique_grades)]
        )
        ax2.set_title("Grade Distribution", fontsize=11, fontweight="bold")

        # 3. Dynamic Subject Performance Overview (if subjects exist)
        if has_subjects:
            sub_labels = [s.name for s in subjects]
            sub_avg_pcts = []

            for sub in subjects:
                total_marks = 0.0
                count = 0
                for s in students:
                    val = s.marks.get(sub.id, s.marks.get(sub.name))
                    if val is not None:
                        total_marks += val
                        count += 1
                if count > 0 and sub.max_marks > 0:
                    avg_score = total_marks / count
                    avg_pct = round((avg_score / sub.max_marks) * 100.0, 1)
                else:
                    avg_pct = 0.0
                sub_avg_pcts.append(avg_pct)

            sub_bars = ax3.bar(sub_labels, sub_avg_pcts, color="#0D9488", edgecolor="#042F2E")
            ax3.set_ylim(0, 105)
            ax3.set_title("Subject Performance (Class Avg %)", fontsize=11, fontweight="bold")
            ax3.set_ylabel("Average Score (%)")
            ax3.grid(axis="y", linestyle=":", alpha=0.6)
            if len(sub_labels) > 3:
                ax3.tick_params(axis="x", rotation=25)

            for bar in sub_bars:
                h = bar.get_height()
                ax3.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 1.5,
                    f"{h:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=8
                )

        plt.tight_layout()
        plt.show()

    def refresh_table(self) -> None:
        """Reload and display all records."""
        self.populate_treeview(self.storage.get_all_students())

    def populate_treeview(self, students_list: List[Student]) -> None:
        """Populate Treeview rows dynamically according to current subjects."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        subjects = self.storage.subject_manager.get_all_subjects()
        sub_ids = [s.id for s in subjects]
        total_max = self.storage.subject_manager.get_total_max_marks()
        max_tot_disp = int(total_max) if total_max.is_integer() else total_max

        for s in students_list:
            row_values = [s.student_id, s.name, s.class_div]

            for sub in subjects:
                m_val = s.marks.get(sub.id, s.marks.get(sub.name, "-"))
                if isinstance(m_val, float) and m_val.is_integer():
                    m_val = int(m_val)
                row_values.append(m_val)

            total_obtained = s.calculate_total_marks(sub_ids)
            tot_disp = int(total_obtained) if total_obtained.is_integer() else total_obtained

            row_values.append(f"{tot_disp} / {max_tot_disp}")
            row_values.append(f"{s.percentage}%")
            row_values.append(s.grade)

            self.tree.insert("", "end", values=tuple(row_values))

        self.lbl_record_count.config(text=f"Total Students: {self.storage.get_total_count()}")

    def clear_form(self) -> None:
        """Reset form fields and selection."""
        self.selected_student_id = None
        self.var_id.set("")
        self.var_name.set("")
        self.var_class.set("")

        for var in self.subject_vars.values():
            var.set("")

        self.var_percentage.set("-- %")
        self.var_grade.set("--")
        self.entry_id.focus_set()
        self.set_status("Form cleared. Ready for new input.")

    def set_status(self, message: str) -> None:
        """Update status bar text."""
        self.lbl_status_text.config(text=message)
