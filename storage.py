"""JSON persistence and storage manager for student records and dynamic subjects."""

import os
import json
import shutil
import re
from typing import List, Dict, Optional, Set, Tuple, Any
from student import Student
from subject import Subject
from validator import (
    DuplicateIDError,
    StudentNotFoundError,
    DuplicateSubjectError,
    SubjectNotFoundError,
)


class SubjectStorageManager:
    """Manages loading, saving, and querying configured academic subjects in JSON format."""

    DEFAULT_SUBJECTS: List[Dict[str, Any]] = [
        {"id": "SUB01", "name": "Advanced Python", "max_marks": 100.0},
        {"id": "SUB02", "name": "DBMS", "max_marks": 100.0},
        {"id": "SUB03", "name": "Computer Networks", "max_marks": 100.0},
    ]

    def __init__(self, data_directory: str = "data", filename: str = "subjects.json"):
        self.data_directory = data_directory
        self.filename = filename
        self.filepath = os.path.join(self.data_directory, self.filename)
        self._subjects: Dict[str, Subject] = {}

        self._ensure_directory_exists()
        self.load_from_file()

    def _ensure_directory_exists(self) -> None:
        """Create data directory if missing."""
        if not os.path.exists(self.data_directory):
            try:
                os.makedirs(self.data_directory, exist_ok=True)
            except OSError as err:
                print(f"[ERROR] Could not create directory '{self.data_directory}': {err}")

    def load_from_file(self) -> None:
        """Load subject definitions from JSON file, initializing defaults if absent or malformed."""
        self._subjects.clear()

        if not os.path.exists(self.filepath):
            self._load_default_subjects()
            self.save_to_file()
            return

        try:
            with open(self.filepath, mode="r", encoding="utf-8") as f:
                raw_data = json.load(f)

            if isinstance(raw_data, list) and raw_data:
                for item in raw_data:
                    try:
                        subject = Subject.from_dict(item)
                        if subject.id:
                            self._subjects[subject.id] = subject
                    except Exception as parse_err:
                        print(f"[WARNING] Skipping malformed subject record: {parse_err}")

            if not self._subjects:
                self._load_default_subjects()
                self.save_to_file()

        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[INFO] Subjects file '{self.filepath}' missing or corrupt. Re-initializing defaults.")
            self._load_default_subjects()
            self.save_to_file()
        except IOError as io_err:
            print(f"[ERROR] Subjects file read failed: {io_err}")

    def save_to_file(self) -> None:
        """Save all subjects to JSON file."""
        self._ensure_directory_exists()
        subject_list = [s.to_dict() for s in self._subjects.values()]
        try:
            with open(self.filepath, mode="w", encoding="utf-8") as f:
                json.dump(subject_list, f, indent=4)
        except IOError as io_err:
            raise IOError(f"Failed to save subject data: {io_err}")

    def _load_default_subjects(self) -> None:
        """Initialize default syllabus subjects."""
        self._subjects.clear()
        for item in self.DEFAULT_SUBJECTS:
            sub = Subject.from_dict(item)
            self._subjects[sub.id] = sub

    def get_all_subjects(self) -> List[Subject]:
        """Return list of all configured subjects."""
        return list(self._subjects.values())

    def get_subject(self, subject_id: str) -> Optional[Subject]:
        """Retrieve subject by ID."""
        return self._subjects.get(subject_id)

    def get_subject_by_name(self, name: str) -> Optional[Subject]:
        """Find subject by name (case-insensitive)."""
        target = name.strip().lower()
        for sub in self._subjects.values():
            if sub.name.strip().lower() == target:
                return sub
        return None

    def add_subject(self, subject: Subject) -> None:
        """Add a new subject after validating ID and name uniqueness."""
        if subject.id in self._subjects:
            raise DuplicateSubjectError(f"Subject with ID '{subject.id}' already exists!")

        existing = self.get_subject_by_name(subject.name)
        if existing:
            raise DuplicateSubjectError(
                f"A subject with name '{subject.name}' already exists (ignoring case)!"
            )

        self._subjects[subject.id] = subject
        self.save_to_file()

    def update_subject(self, subject: Subject) -> None:
        """Update existing subject details."""
        if subject.id not in self._subjects:
            raise SubjectNotFoundError(f"Subject with ID '{subject.id}' not found.")

        # Check name conflict with other subjects
        for sid, existing in self._subjects.items():
            if sid != subject.id and existing.name.strip().lower() == subject.name.strip().lower():
                raise DuplicateSubjectError(
                    f"Another subject already uses the name '{subject.name}'."
                )

        self._subjects[subject.id] = subject
        self.save_to_file()

    def delete_subject(self, subject_id: str) -> Subject:
        """Remove a subject by ID."""
        if subject_id not in self._subjects:
            raise SubjectNotFoundError(f"Subject with ID '{subject_id}' not found.")

        removed = self._subjects.pop(subject_id)
        self.save_to_file()
        return removed

    def generate_subject_id(self) -> str:
        """Generate a next available stable subject ID (e.g., SUB04)."""
        highest_num = 0
        for sid in self._subjects.keys():
            match = re.match(r"^SUB(\d+)$", sid.upper())
            if match:
                num = int(match.group(1))
                if num > highest_num:
                    highest_num = num

        next_num = highest_num + 1
        new_id = f"SUB{next_num:02d}"
        # Ensure absolute uniqueness
        while new_id in self._subjects:
            next_num += 1
            new_id = f"SUB{next_num:02d}"
        return new_id

    def get_total_max_marks(self) -> float:
        """Sum of maximum marks across all configured subjects."""
        if not self._subjects:
            return 0.0
        return round(sum(s.max_marks for s in self._subjects.values()), 2)

    def get_subject_ids(self) -> List[str]:
        """Return list of all configured subject IDs."""
        return list(self._subjects.keys())


class StudentStorageManager:
    """Manages loading, saving, migration, and querying student records in JSON format."""

    def __init__(
        self,
        data_directory: str = "data",
        filename: str = "students.json",
        subjects_filename: str = "subjects.json",
        subject_manager: Optional[SubjectStorageManager] = None
    ):
        self.data_directory = data_directory
        self.filename = filename
        self.filepath = os.path.join(self.data_directory, self.filename)
        self._students: Dict[str, Student] = {}

        self.subject_manager: SubjectStorageManager = (
            subject_manager or SubjectStorageManager(self.data_directory, subjects_filename)
        )

        self._ensure_directory_exists()
        self.load_from_file()

    def _ensure_directory_exists(self) -> None:
        """Create data directory if missing."""
        if not os.path.exists(self.data_directory):
            try:
                os.makedirs(self.data_directory, exist_ok=True)
            except OSError as err:
                print(f"[ERROR] Could not create directory '{self.data_directory}': {err}")

    def load_from_file(self) -> None:
        """Load student records, performing automatic data migration if legacy format detected."""
        self._students.clear()

        if not os.path.exists(self.filepath):
            self._load_sample_data()
            self.save_to_file()
            return

        try:
            with open(self.filepath, mode="r", encoding="utf-8") as f:
                raw_data = json.load(f)

            if isinstance(raw_data, list):
                # Check whether migration is needed
                if self._needs_migration(raw_data):
                    print("[INFO] Legacy student records detected. Initiating migration to stable subject IDs...")
                    raw_data = self._migrate_legacy_records(raw_data)

                max_possible = self.subject_manager.get_total_max_marks()
                for item in raw_data:
                    try:
                        student = Student.from_dict(item, max_possible_marks=max_possible)
                        self._students[student.student_id] = student
                    except Exception as parse_err:
                        print(f"[WARNING] Skipping invalid student item: {parse_err}")

        except (FileNotFoundError, json.JSONDecodeError):
            self._load_sample_data()
            self.save_to_file()
        except IOError as io_err:
            print(f"[ERROR] Student file read failed: {io_err}")

    def _needs_migration(self, raw_data: List[Dict[str, Any]]) -> bool:
        """Check if any student record has marks keyed by subject name rather than subject ID."""
        subject_ids = set(self.subject_manager.get_subject_ids())
        for item in raw_data:
            marks = item.get("marks", {})
            if isinstance(marks, dict):
                for key in marks.keys():
                    if key not in subject_ids:
                        return True
        return False

    def _migrate_legacy_records(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Migrate student records with legacy subject names to stable subject IDs.
        Always creates a backup of the original file prior to migrating.
        """
        # 1. Back up existing file
        backup_filename = f"{os.path.splitext(self.filename)[0]}_backup.json"
        backup_path = os.path.join(self.data_directory, backup_filename)
        try:
            shutil.copy2(self.filepath, backup_path)
            print(f"[INFO] Backup successfully created at '{backup_path}'.")
        except Exception as backup_err:
            print(f"[WARNING] Could not create backup file: {backup_err}")

        # 2. Build name-to-id mapping
        subjects = self.subject_manager.get_all_subjects()
        name_to_id: Dict[str, str] = {}
        for sub in subjects:
            name_to_id[sub.name.lower()] = sub.id

        # Common legacy aliases
        name_to_id["advanced python"] = name_to_id.get("advanced python", "SUB01")
        name_to_id["dbms"] = name_to_id.get("dbms", "SUB02")
        name_to_id["computer networks"] = name_to_id.get("computer networks", "SUB03")
        name_to_id["cn"] = name_to_id.get("computer networks", "SUB03")

        migrated_list: List[Dict[str, Any]] = []

        try:
            for item in raw_data:
                marks = item.get("marks", {})
                new_marks: Dict[str, float] = {}

                for key, val in marks.items():
                    k_clean = str(key).strip()
                    k_lower = k_clean.lower()
                    try:
                        numeric_val = float(val)
                    except (ValueError, TypeError):
                        numeric_val = 0.0

                    if k_lower in name_to_id:
                        new_marks[name_to_id[k_lower]] = numeric_val
                    elif k_clean in self.subject_manager.get_subject_ids():
                        new_marks[k_clean] = numeric_val
                    else:
                        # Unknown subject name: dynamically register it as a new subject
                        new_id = self.subject_manager.generate_subject_id()
                        new_sub = Subject(subject_id=new_id, name=k_clean, max_marks=100.0)
                        self.subject_manager.add_subject(new_sub)
                        name_to_id[k_lower] = new_id
                        new_marks[new_id] = numeric_val

                # Recalculate percentage and grade based on configured subjects
                max_possible = self.subject_manager.get_total_max_marks()
                total = sum(new_marks.values())
                pct = round((total / max_possible) * 100.0, 2) if max_possible > 0 else 0.0

                grade = "F"
                for min_score, g_letter in Student.GRADE_SCALE:
                    if pct >= min_score:
                        grade = g_letter
                        break

                migrated_item = {
                    "student_id": item.get("student_id", ""),
                    "name": item.get("name", ""),
                    "class_div": item.get("class_div", ""),
                    "marks": new_marks,
                    "percentage": pct,
                    "grade": grade,
                }
                migrated_list.append(migrated_item)

            # Save migrated data immediately
            with open(self.filepath, mode="w", encoding="utf-8") as f:
                json.dump(migrated_list, f, indent=4)

            print("[INFO] Data migration completed successfully.")
            return migrated_list

        except Exception as mig_err:
            print(f"[ERROR] Migration failed: {mig_err}. Retaining original data.")
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.filepath)
            raise RuntimeError(f"Data migration failed: {mig_err}. Original file restored.")

    def save_to_file(self) -> None:
        """Save all student records to JSON file."""
        self._ensure_directory_exists()
        records_list = [student.to_dict() for student in self._students.values()]

        try:
            with open(self.filepath, mode="w", encoding="utf-8") as f:
                json.dump(records_list, f, indent=4)
        except IOError as io_err:
            raise IOError(f"Failed to save student data: {io_err}")

    def _load_sample_data(self) -> None:
        """Initialize sample records using configured subject IDs."""
        sub_ids = self.subject_manager.get_subject_ids()
        id1 = sub_ids[0] if len(sub_ids) > 0 else "SUB01"
        id2 = sub_ids[1] if len(sub_ids) > 1 else "SUB02"
        id3 = sub_ids[2] if len(sub_ids) > 2 else "SUB03"

        max_possible = self.subject_manager.get_total_max_marks()

        sample_students = [
            Student(
                student_id="TY01",
                name="Aarav Sharma",
                class_div="TY CSE A",
                marks={id1: 88.0, id2: 92.0, id3: 85.0},
                max_possible_marks=max_possible
            ),
            Student(
                student_id="TY02",
                name="Diya Kulkarni",
                class_div="TY CSE A",
                marks={id1: 95.0, id2: 90.0, id3: 94.0},
                max_possible_marks=max_possible
            ),
            Student(
                student_id="TY03",
                name="Rohan Patil",
                class_div="TY CSE B",
                marks={id1: 64.0, id2: 70.0, id3: 68.0},
                max_possible_marks=max_possible
            ),
            Student(
                student_id="TY04",
                name="Sneha Deshmukh",
                class_div="TY CSE B",
                marks={id1: 78.0, id2: 82.0, id3: 75.0},
                max_possible_marks=max_possible
            )
        ]
        for s in sample_students:
            self._students[s.student_id] = s

    def add_student(self, student: Student) -> None:
        """Add a new student record."""
        if student.student_id in self._students:
            raise DuplicateIDError(f"Student with ID '{student.student_id}' already exists!")

        # Ensure percentage and grade are aligned with current configured subjects
        max_possible = self.subject_manager.get_total_max_marks()
        sub_ids = self.subject_manager.get_subject_ids()
        student.recalculate(max_possible, sub_ids)

        self._students[student.student_id] = student
        self.save_to_file()

    def update_student(self, student: Student) -> None:
        """Update an existing student record."""
        if student.student_id not in self._students:
            raise StudentNotFoundError(f"Student ID '{student.student_id}' not found.")

        max_possible = self.subject_manager.get_total_max_marks()
        sub_ids = self.subject_manager.get_subject_ids()
        student.recalculate(max_possible, sub_ids)

        self._students[student.student_id] = student
        self.save_to_file()

    def delete_student(self, student_id: str) -> Student:
        """Delete student record by ID."""
        if student_id not in self._students:
            raise StudentNotFoundError(f"Student ID '{student_id}' not found.")
        removed = self._students.pop(student_id)
        self.save_to_file()
        return removed

    def get_student(self, student_id: str) -> Optional[Student]:
        """Retrieve student record by ID."""
        return self._students.get(student_id)

    def get_all_students(self) -> List[Student]:
        """Return list of all student objects."""
        return list(self._students.values())

    def search_students(self, query: str) -> List[Student]:
        """Search students by matching ID or Name (case-insensitive)."""
        clean_query = query.strip().lower()
        if not clean_query:
            return self.get_all_students()

        return [
            s for s in self._students.values()
            if clean_query in s.student_id.lower() or clean_query in s.name.lower()
        ]

    def sort_students(self, by: str = "percentage", reverse: bool = True) -> List[Student]:
        """Sort students using a lambda key function."""
        student_list = list(self._students.values())
        if by == "percentage":
            return sorted(student_list, key=lambda s: s.percentage, reverse=reverse)
        elif by == "name":
            return sorted(student_list, key=lambda s: s.name.lower(), reverse=reverse)
        elif by == "id":
            return sorted(student_list, key=lambda s: s.student_id, reverse=reverse)
        return student_list

    def get_unique_classes(self) -> Set[str]:
        """Return set of unique class/division names."""
        return {student.class_div for student in self._students.values()}

    def get_total_count(self) -> int:
        """Return total student count."""
        return len(self._students)

    def check_subject_max_marks_conflict(
        self,
        subject_id: str,
        new_max_marks: float
    ) -> Optional[Tuple[Student, float]]:
        """
        Check if any student currently has a mark exceeding new_max_marks for subject_id.
        Returns (conflicting_student, mark) or None if no conflict exists.
        """
        for student in self._students.values():
            mark = student.marks.get(subject_id)
            if mark is not None and mark > new_max_marks:
                return student, mark
        return None

    def remove_subject_from_students(self, subject_id: str) -> None:
        """
        Remove subject from all student records and recalculate their percentage and grade.
        Called after user confirms subject deletion.
        """
        max_possible = self.subject_manager.get_total_max_marks()
        sub_ids = self.subject_manager.get_subject_ids()

        for student in self._students.values():
            if subject_id in student.marks:
                del student.marks[subject_id]
            student.recalculate(max_possible, sub_ids)

        self.save_to_file()

    def recalculate_all_students(self) -> None:
        """
        Recalculate percentage and grade for all students using current subjects.
        Called after subject max marks are edited.
        """
        max_possible = self.subject_manager.get_total_max_marks()
        sub_ids = self.subject_manager.get_subject_ids()

        for student in self._students.values():
            student.recalculate(max_possible, sub_ids)

        self.save_to_file()
