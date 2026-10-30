"""Input validation and custom exception definitions for Student Record System."""

import re
from typing import Optional, Sequence


class ValidationError(Exception):
    """Raised when form input fails validation."""
    pass


class DuplicateIDError(Exception):
    """Raised when student ID already exists."""
    pass


class StudentNotFoundError(Exception):
    """Raised when student record is not found."""
    pass


class DuplicateSubjectError(Exception):
    """Raised when a subject name already exists."""
    pass


class SubjectNotFoundError(Exception):
    """Raised when a subject record is not found."""
    pass


def validate_student_id(student_id: str) -> str:
    """Validate student ID: 2-15 alphanumeric characters (e.g., TY01, S101)."""
    cleaned_id = str(student_id).strip()
    if not cleaned_id:
        raise ValidationError("Student ID cannot be empty.")
    if not re.match(r"^[A-Za-z0-9\-_]{2,15}$", cleaned_id):
        raise ValidationError("Invalid Student ID! Must be 2-15 alphanumeric characters.")
    return cleaned_id.upper()


def validate_name(name: str) -> str:
    """Validate student name: only letters, dots, and spaces (2-50 chars)."""
    cleaned_name = str(name).strip()
    if not cleaned_name:
        raise ValidationError("Student Name cannot be empty.")
    if not re.match(r"^[A-Za-z\s.]{2,50}$", cleaned_name):
        raise ValidationError("Invalid Name! Name must contain only alphabets and spaces.")
    return cleaned_name.title()


def validate_class_div(class_div: str) -> str:
    """Validate class/division: 1-15 characters."""
    cleaned_class = str(class_div).strip()
    if not cleaned_class:
        raise ValidationError("Class / Division cannot be empty.")
    if not re.match(r"^[A-Za-z0-9\s\-_]{1,15}$", cleaned_class):
        raise ValidationError("Invalid Class/Division format.")
    return cleaned_class.upper()


def validate_mark(subject_name: str, mark_value, max_marks: float = 100.0) -> float:
    """
    Validate subject marks: numeric value between 0 and configured maximum marks.
    Defaults to 100.0 for backward compatibility.
    """
    try:
        val = float(mark_value)
    except (ValueError, TypeError):
        raise ValidationError(f"Marks for '{subject_name}' must be a number.")

    if val < 0.0 or val > max_marks:
        max_str = int(max_marks) if float(max_marks).is_integer() else max_marks
        raise ValidationError(f"Marks for '{subject_name}' must be between 0 and {max_str}.")
    return round(val, 2)


def validate_subject_name(name: str, existing_names: Optional[Sequence[str]] = None) -> str:
    """
    Validate subject name: non-empty, 2-50 characters, and case-insensitive uniqueness.
    """
    cleaned_name = str(name).strip()
    if not cleaned_name:
        raise ValidationError("Subject name cannot be empty.")
    if len(cleaned_name) < 2 or len(cleaned_name) > 50:
        raise ValidationError("Subject name must be between 2 and 50 characters.")
    if not re.match(r"^[A-Za-z0-9\s\-_().+&]{2,50}$", cleaned_name):
        raise ValidationError("Subject name contains invalid characters.")

    if existing_names:
        for existing in existing_names:
            if cleaned_name.lower() == str(existing).strip().lower():
                raise DuplicateSubjectError(
                    f"A subject named '{cleaned_name}' already exists (ignoring letter case)."
                )
    return cleaned_name


def validate_max_marks(max_marks_value) -> float:
    """Validate maximum marks: positive number greater than zero."""
    try:
        val = float(max_marks_value)
    except (ValueError, TypeError):
        raise ValidationError("Maximum marks must be a valid number.")

    if val <= 0.0:
        raise ValidationError("Maximum marks must be a positive number greater than 0.")
    if val > 1000.0:
        raise ValidationError("Maximum marks cannot exceed 1000.")
    return round(val, 2)
