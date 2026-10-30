# Student Record Management System

A desktop application built with Python and Tkinter for managing student academic records with **Dynamic Subject Management**. Developed as a college mini-project for **Advanced Programming Concepts (Python)**.

---

## Features

- **Dynamic Subject Management:** Create, rename, edit maximum marks, or delete subjects at runtime without touching Python code.
- **Dynamic Student Form:** Automatically generates mark input fields for all configured subjects in a scrollable area.
- **Dynamic Records Table:** Dynamically generates subject columns in the `ttk.Treeview` table, displaying total marks out of dynamic maximum possible marks.
- **Dynamic Grade & Percentage Calculation:** Computes Total Marks as sum across active subjects, Maximum Possible Marks, and Percentage = `(Total Marks / Maximum Possible Marks) * 100`.
- **Conflict Prevention on Edit:** Validates that maximum marks cannot be lowered below any existing student mark, preventing data corruption.
- **Add Student:** Register new student records with ID, name, class/division, and subject marks.
- **View Records:** Display student records in an interactive table with vertical and horizontal scrollbars.
- **Search & Filter:** Search students by ID or Name.
- **Update Record:** Select any record to modify details and save changes.
- **Delete Record:** Remove records with a confirmation prompt.
- **Preview Tool:** Preview percentage and grade before saving.
- **Data Visualization:** Interactive Matplotlib charts displaying percentage comparisons (bar chart), grade distribution (pie chart), and subject-specific class performance.
- **Local Persistence & Automatic Migration:** Saves and loads data automatically from local JSON files (`data/students.json` and `data/subjects.json`). Automatically migrates legacy fixed-subject records and creates backups prior to migration.
- **Sort by Performance:** Sort records by percentage in descending order.

---

## Project Structure

```
Mini_Project/
├── main.py              # Application entry point & DPI setup
├── gui.py               # Tkinter GUI layout, Treeview table, and Subject Manager dialog
├── subject.py           # Subject class model (ID, Name, Max Marks)
├── student.py           # Person (base class) and Student (derived class) models
├── storage.py           # JSON persistence, CRUD operations, migration & backup managers
├── validator.py         # Input validation, regex rules, and custom exceptions
├── README.md            # Project documentation
└── data/
    ├── students.json    # JSON storage file for student records
    ├── subjects.json    # JSON storage file for configured subjects
    └── students_backup.json # Safe backup created before migration
```

---

## File Overview

| File | Description |
| :--- | :--- |
| `main.py` | Initializes High-DPI display settings and launches the application. |
| `gui.py` | Builds the Tkinter user interface, dynamic forms, Treeview tables, Matplotlib analytics, and the `SubjectManagementDialog`. |
| `subject.py` | Contains the OOP `Subject` model with stable IDs, encapsulation, getters, setters, and JSON serialization. |
| `student.py` | Contains OOP models (`Person` base class, `Student` child class), inheritance, and dynamic grading logic. |
| `storage.py` | Manages `SubjectStorageManager` and `StudentStorageManager` with automatic backup and migration. |
| `validator.py` | Validates student IDs, names, marks (0 to max marks), and subject names (case-insensitive uniqueness). |
| `data/students.json` | Stores student data locally in JSON format with stable subject IDs. |
| `data/subjects.json` | Stores curriculum subjects configuration (ID, name, max marks). |

---

## How to Run

### Requirements
- Python 3.8+
- Matplotlib:
  ```bash
  pip install matplotlib
  ```

### Run Application
```bash
python main.py
```

### Run Verification Tests
```bash
python test_system.py
```
