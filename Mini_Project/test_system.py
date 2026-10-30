"""
test_system.py
Unit and integration test script for Student Record Management System.
Verifies all core requirements, dynamic subject management, and syllabus features without launching the GUI.
"""

import os
import shutil
import json
from student import Person, Student
from subject import Subject
from storage import StudentStorageManager, SubjectStorageManager
from validator import (
    validate_student_id,
    validate_name,
    validate_class_div,
    validate_mark,
    validate_subject_name,
    validate_max_marks,
    ValidationError,
    DuplicateIDError,
    StudentNotFoundError,
    DuplicateSubjectError,
    SubjectNotFoundError,
)


def run_tests():
    print("==================================================")
    print("RUNNING SYLLABUS & FEATURE VERIFICATION TESTS")
    print("==================================================")

    # 1. Test OOP: Inheritance and Polymorphism
    print("[TEST 1] Testing OOP (Person base class, Student child class, Polymorphism)...")
    person = Person("Test Person")
    student = Student("T101", "Aarav Sharma", "TY CSE A", {"Advanced Python": 95, "DBMS": 90, "Computer Networks": 88})
    
    assert isinstance(student, Person), "Student should inherit from Person!"
    assert student.name == "Aarav Sharma"
    assert student.student_id == "T101"
    
    # Polymorphism: get_details() should return different keys
    person_details = person.get_details()
    student_details = student.get_details()
    assert "student_id" not in person_details
    assert "student_id" in student_details
    print("  -> Passed: Inheritance and Polymorphism verified.")

    # 2. Test Percentage & Grade Calculation
    print("[TEST 2] Testing Percentage and Grade Calculations...")
    # 95 + 90 + 88 = 273 / 3 = 91.0 % -> Grade A+
    assert student.calculate_total_marks() == 273.0
    assert student.percentage == 91.0
    assert student.grade == "A+"

    # Test boundary grade values
    s_bplus = Student("T102", "Diya", "TY CSE A", {"Sub1": 75, "Sub2": 72, "Sub3": 78})
    assert s_bplus.percentage == 75.0
    assert s_bplus.grade == "B+"

    s_fail = Student("T103", "Fail Case", "TY CSE A", {"Sub1": 30, "Sub2": 35, "Sub3": 38})
    assert s_fail.percentage == 34.33
    assert s_fail.grade == "F"
    print("  -> Passed: Percentage and Grade logic correct.")

    # 3. Test Regex Validation
    print("[TEST 3] Testing Regular Expressions input validation...")
    # Valid
    assert validate_student_id("TY01") == "TY01"
    assert validate_name("Aarav Sharma") == "Aarav Sharma"
    assert validate_class_div("TY CSE-A") == "TY CSE-A"
    assert validate_mark("Python", 85) == 85.0

    # Invalid student ID
    try:
        validate_student_id("!!Invalid##")
        assert False, "Should have raised ValidationError for invalid ID"
    except ValidationError:
        pass

    # Invalid student Name (numbers in name)
    try:
        validate_name("John123")
        assert False, "Should have raised ValidationError for numbers in name"
    except ValidationError:
        pass

    # Invalid marks (< 0 or > 100)
    try:
        validate_mark("DBMS", 105)
        assert False, "Should have raised ValidationError for marks > 100"
    except ValidationError:
        pass
    print("  -> Passed: Regex and input validations work as expected.")

    # 4. Test Storage & File Handling (JSON Persistence)
    print("[TEST 4] Testing Storage Manager (JSON persistence, CRUD)...")
    test_dir = "test_data"
    test_file = "test_students.json"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    manager = StudentStorageManager(data_directory=test_dir, filename=test_file)
    assert os.path.exists(os.path.join(test_dir, test_file)), "Storage file should be created automatically!"

    # Add student
    manager.add_student(student)
    assert manager.get_student("T101") is not None
    assert manager.get_student("T101").name == "Aarav Sharma"

    # Duplicate check
    try:
        manager.add_student(student)
        assert False, "Should raise DuplicateIDError"
    except DuplicateIDError:
        pass

    # Update student
    updated = Student("T101", "Aarav Sharma Updated", "TY CSE B", {"Advanced Python": 98, "DBMS": 92, "Computer Networks": 95})
    manager.update_student(updated)
    assert manager.get_student("T101").name == "Aarav Sharma Updated"
    assert manager.get_student("T101").class_div == "TY CSE B"

    # Search student
    search_res = manager.search_students("Updated")
    assert len(search_res) == 1 and search_res[0].student_id == "T101"

    # Sorting with lambda
    top_students = manager.sort_students(by="percentage", reverse=True)
    assert len(top_students) >= 1

    # Delete student
    deleted = manager.delete_student("T101")
    assert deleted.student_id == "T101"
    assert manager.get_student("T101") is None

    # Test Reloading from Disk
    manager2 = StudentStorageManager(data_directory=test_dir, filename=test_file)
    assert manager2.get_student("T101") is None

    # Clean up test data
    shutil.rmtree(test_dir)
    print("  -> Passed: File handling and persistence verified.")

    # 5. Test Dynamic Subject Model & Encapsulation
    print("[TEST 5] Testing Subject Model & Encapsulation...")
    sub = Subject(subject_id="SUB01", name="Advanced Python", max_marks=100.0)
    assert sub.id == "SUB01"
    assert sub.name == "Advanced Python"
    assert sub.max_marks == 100.0

    # Test property setters
    sub.name = "Advanced Python Programming"
    assert sub.name == "Advanced Python Programming"
    sub.max_marks = 80.0
    assert sub.max_marks == 80.0

    # Test invalid setter values
    try:
        sub.name = "   "
        assert False, "Should reject empty subject name"
    except ValueError:
        pass

    try:
        sub.max_marks = -10
        assert False, "Should reject negative max marks"
    except ValueError:
        pass

    # Test serialization
    sub_dict = sub.to_dict()
    assert sub_dict["id"] == "SUB01"
    assert sub_dict["name"] == "Advanced Python Programming"
    assert sub_dict["max_marks"] == 80.0

    sub_restored = Subject.from_dict(sub_dict)
    assert sub_restored.id == "SUB01"
    assert sub_restored.name == "Advanced Python Programming"
    assert sub_restored.max_marks == 80.0
    print("  -> Passed: Subject model properties, setters, and serialization verified.")

    # 6. Test Dynamic Subject Input Validation
    print("[TEST 6] Testing Dynamic Subject Validation...")
    # Non-empty and length
    assert validate_subject_name("Operating Systems") == "Operating Systems"
    try:
        validate_subject_name("")
        assert False, "Should reject empty subject name"
    except ValidationError:
        pass

    # Case-insensitive duplicate check
    existing = ["Advanced Python", "DBMS", "Computer Networks"]
    try:
        validate_subject_name("dbms", existing_names=existing)
        assert False, "Should reject case-insensitive duplicate subject name"
    except DuplicateSubjectError:
        pass

    try:
        validate_subject_name("ADVANCED PYTHON", existing_names=existing)
        assert False, "Should reject uppercase duplicate subject name"
    except DuplicateSubjectError:
        pass

    # Max marks validation
    assert validate_max_marks(100) == 100.0
    assert validate_max_marks("75.5") == 75.5
    try:
        validate_max_marks(0)
        assert False, "Should reject 0 max marks"
    except ValidationError:
        pass

    try:
        validate_max_marks(-25)
        assert False, "Should reject negative max marks"
    except ValidationError:
        pass

    # Dynamic mark range validation
    assert validate_mark("Operating Systems", 45, max_marks=50.0) == 45.0
    try:
        validate_mark("Operating Systems", 55, max_marks=50.0)
        assert False, "Should reject mark exceeding configured max_marks"
    except ValidationError:
        pass
    print("  -> Passed: Subject name, duplicate prevention, and dynamic mark validation verified.")

    # 7. Test SubjectStorageManager (CRUD, Stable IDs, Persistence)
    print("[TEST 7] Testing SubjectStorageManager (CRUD, Stable ID Generation)...")
    sub_test_dir = "test_subject_data"
    sub_test_file = "test_subjects.json"
    if os.path.exists(sub_test_dir):
        shutil.rmtree(sub_test_dir)

    sub_mgr = SubjectStorageManager(data_directory=sub_test_dir, filename=sub_test_file)
    default_subs = sub_mgr.get_all_subjects()
    assert len(default_subs) == 3, "Default subjects should be initialized"

    # Add new subject
    new_sub_id = sub_mgr.generate_subject_id()
    assert new_sub_id == "SUB04", f"Expected SUB04, got {new_sub_id}"
    new_sub = Subject(new_sub_id, "Cloud Computing", 100.0)
    sub_mgr.add_subject(new_sub)
    assert sub_mgr.get_subject("SUB04") is not None
    assert sub_mgr.get_subject("SUB04").name == "Cloud Computing"

    # Edit subject name (rename)
    new_sub.name = "Distributed Cloud Systems"
    sub_mgr.update_subject(new_sub)
    assert sub_mgr.get_subject("SUB04").name == "Distributed Cloud Systems"

    # Total max marks
    # 3 defaults * 100 + 100 = 400
    assert sub_mgr.get_total_max_marks() == 400.0

    # Delete subject
    deleted_sub = sub_mgr.delete_subject("SUB04")
    assert deleted_sub.id == "SUB04"
    assert sub_mgr.get_subject("SUB04") is None
    assert sub_mgr.get_total_max_marks() == 300.0

    # Clean up test directory
    shutil.rmtree(sub_test_dir)
    print("  -> Passed: SubjectStorageManager CRUD and ID generation verified.")

    # 8. Test Dynamic Calculations with Custom Max Marks & Zero-Subject Edge Case
    print("[TEST 8] Testing Dynamic Calculations with Non-100 Max Marks & Edge Cases...")
    # Subject 1: Max 50, Student scored 45
    # Subject 2: Max 75, Student scored 60
    # Subject 3: Max 100, Student scored 80
    # Total obtained = 45 + 60 + 80 = 185
    # Total possible = 50 + 75 + 100 = 225
    # Percentage = (185 / 225) * 100 = 82.22% -> Grade A
    s_dyn = Student(
        student_id="D101",
        name="Dynamic Student",
        class_div="TY CSE A",
        marks={"S1": 45.0, "S2": 60.0, "S3": 80.0},
        max_possible_marks=225.0
    )
    assert s_dyn.calculate_total_marks() == 185.0
    assert s_dyn.percentage == 82.22
    assert s_dyn.grade == "A"

    # Zero subjects edge case (no division by zero)
    s_empty = Student(
        student_id="EMPTY",
        name="Empty Student",
        class_div="TY CSE",
        marks={},
        max_possible_marks=0.0
    )
    assert s_empty.calculate_total_marks() == 0.0
    assert s_empty.percentage == 0.0
    assert s_empty.grade == "F"
    print("  -> Passed: Dynamic percentage calculations and zero-division safety verified.")

    # 9. Test Subject Edit Conflict Detection
    print("[TEST 9] Testing Subject Edit Conflict Detection...")
    conflict_dir = "test_conflict_data"
    if os.path.exists(conflict_dir):
        shutil.rmtree(conflict_dir)

    c_mgr = StudentStorageManager(data_directory=conflict_dir, filename="conflict_students.json")
    for sid in list(c_mgr._students.keys()):
        c_mgr.delete_student(sid)

    # Add a student with 85 marks in SUB01
    s_conflict = Student(
        student_id="C101",
        name="Conflict Student",
        class_div="TY CSE A",
        marks={"SUB01": 85.0, "SUB02": 70.0, "SUB03": 75.0},
        max_possible_marks=300.0
    )
    c_mgr.add_student(s_conflict)

    # Conflict check: Reducing max marks to 80 should detect conflict because student has 85
    conflict_res = c_mgr.check_subject_max_marks_conflict("SUB01", 80.0)
    assert conflict_res is not None, "Should detect conflict when reducing max marks below student mark"
    conflicting_student, mark = conflict_res
    assert conflicting_student.student_id == "C101"
    assert mark == 85.0

    # Conflict check: Setting max marks to 90 should have NO conflict
    no_conflict_res = c_mgr.check_subject_max_marks_conflict("SUB01", 90.0)
    assert no_conflict_res is None, "Should not detect conflict when max marks >= student mark"

    shutil.rmtree(conflict_dir)
    print("  -> Passed: Subject edit conflict detection verified.")

    # 10. Test Automatic Migration & Backup of Legacy Records
    print("[TEST 10] Testing Data Migration & Automatic Backup...")
    mig_dir = "test_mig_data"
    if os.path.exists(mig_dir):
        shutil.rmtree(mig_dir)
    os.makedirs(mig_dir, exist_ok=True)

    legacy_records = [
        {
            "student_id": "LEG01",
            "name": "Legacy Student",
            "class_div": "TY CSE A",
            "marks": {
                "Advanced Python": 90.0,
                "DBMS": 85.0,
                "Computer Networks": 88.0
            },
            "percentage": 87.67,
            "grade": "A"
        }
    ]
    legacy_file = os.path.join(mig_dir, "students.json")
    with open(legacy_file, "w", encoding="utf-8") as f:
        json.dump(legacy_records, f, indent=4)

    # Initialize manager which will detect legacy format and perform migration
    mig_mgr = StudentStorageManager(data_directory=mig_dir, filename="students.json")

    # 1. Verify backup file was created
    backup_file = os.path.join(mig_dir, "students_backup.json")
    assert os.path.exists(backup_file), "Backup file 'students_backup.json' must be created before migration!"

    # 2. Verify migrated student uses stable subject IDs
    mig_student = mig_mgr.get_student("LEG01")
    assert mig_student is not None
    assert "SUB01" in mig_student.marks, "Legacy 'Advanced Python' should be mapped to 'SUB01'"
    assert "SUB02" in mig_student.marks, "Legacy 'DBMS' should be mapped to 'SUB02'"
    assert "SUB03" in mig_student.marks, "Legacy 'Computer Networks' should be mapped to 'SUB03'"
    assert mig_student.marks["SUB01"] == 90.0
    assert mig_student.marks["SUB02"] == 85.0
    assert mig_student.marks["SUB03"] == 88.0
    assert mig_student.percentage == 87.67
    assert mig_student.grade == "A"

    # 3. Test Renaming Subject: Changing subject name must NOT lose marks
    sub1 = mig_mgr.subject_manager.get_subject("SUB01")
    sub1.name = "Modern Python Programming"
    mig_mgr.subject_manager.update_subject(sub1)

    # Reload from storage and check marks are preserved
    mig_mgr_reloaded = StudentStorageManager(data_directory=mig_dir, filename="students.json")
    reloaded_student = mig_mgr_reloaded.get_student("LEG01")
    assert reloaded_student.marks["SUB01"] == 90.0, "Marks must be preserved using stable subject ID upon renaming!"

    shutil.rmtree(mig_dir)
    print("  -> Passed: Data migration, backup creation, and subject renaming mark-preservation verified.")

    print("==================================================")
    print("ALL 10 TESTS PASSED SUCCESSFULLY! (100% COMPLIANT)")
    print("==================================================")


if __name__ == "__main__":
    run_tests()
