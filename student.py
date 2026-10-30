"""Student and Person class models with OOP inheritance, polymorphism, and dynamic grading."""

from typing import Dict, Any, Tuple, Optional, Sequence


class Person:
    """Base class representing a person."""

    def __init__(self, name: str):
        self._name: str = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def get_details(self) -> Dict[str, Any]:
        """Return basic person details."""
        return {"name": self._name}

    def __str__(self) -> str:
        return f"Person(name={self._name})"


class Student(Person):
    """Student class inheriting from Person with dynamic subject marks and grade calculations."""

    # Grade thresholds: (minimum_percentage, grade)
    GRADE_SCALE: Tuple[Tuple[float, str], ...] = (
        (90.0, "A+"),
        (80.0, "A"),
        (70.0, "B+"),
        (60.0, "B"),
        (50.0, "C"),
        (40.0, "D"),
        (0.0,  "F"),
    )

    def __init__(
        self,
        student_id: str,
        name: str,
        class_div: str,
        marks: Dict[str, float],
        percentage: Optional[float] = None,
        grade: Optional[str] = None,
        max_possible_marks: Optional[float] = None
    ):
        super().__init__(name)
        self._student_id: str = student_id
        self._class_div: str = class_div
        self._marks: Dict[str, float] = dict(marks) if marks else {}

        if percentage is not None and grade is not None:
            self._percentage: float = round(float(percentage), 2)
            self._grade: str = str(grade)
        else:
            self._percentage: float = self.calculate_percentage(max_possible_marks)
            self._grade: str = self.calculate_grade(self._percentage)

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def class_div(self) -> str:
        return self._class_div

    @class_div.setter
    def class_div(self, value: str):
        self._class_div = value

    @property
    def marks(self) -> Dict[str, float]:
        return self._marks

    @marks.setter
    def marks(self, new_marks: Dict[str, float]):
        self._marks = dict(new_marks) if new_marks else {}
        self._percentage = self.calculate_percentage()
        self._grade = self.calculate_grade(self._percentage)

    @property
    def percentage(self) -> float:
        return self._percentage

    @property
    def grade(self) -> str:
        return self._grade

    def calculate_total_marks(self, subject_ids: Optional[Sequence[str]] = None) -> float:
        """
        Calculate total marks obtained across subjects.
        If subject_ids is provided, sums marks for those subject IDs.
        Falls back gracefully if marks are keyed by subject names.
        """
        if not self._marks:
            return 0.0

        if subject_ids is not None:
            matching_sum = 0.0
            found_any = False
            for sid in subject_ids:
                if sid in self._marks:
                    matching_sum += self._marks[sid]
                    found_any = True

            if found_any:
                return round(matching_sum, 2)

            # Fallback if marks dict uses subject names rather than IDs
            return round(sum(self._marks.values()), 2)

        return round(sum(self._marks.values()), 2)

    def calculate_percentage(
        self,
        max_possible_marks: Optional[float] = None,
        subject_ids: Optional[Sequence[str]] = None
    ) -> float:
        """
        Calculate percentage: (Total Marks / Maximum Possible Marks) * 100.
        Handles zero-subject edge case safely without division by zero.
        """
        if not self._marks:
            return 0.0

        total_obtained = self.calculate_total_marks(subject_ids)

        if max_possible_marks is not None:
            if max_possible_marks <= 0.0:
                return 0.0
            return round((total_obtained / max_possible_marks) * 100.0, 2)

        # Default fallback (legacy 100 marks per subject)
        divisor = len(self._marks) * 100.0
        if divisor <= 0.0:
            return 0.0
        return round((total_obtained / divisor) * 100.0, 2)

    def calculate_grade(self, percentage_val: Optional[float] = None) -> str:
        """
        Assign letter grade based on percentage using GRADE_SCALE.
        Encapsulated in one clearly named method for maintainability and viva explanation.
        """
        pct = self._percentage if percentage_val is None else percentage_val
        for min_score, letter_grade in self.GRADE_SCALE:
            if pct >= min_score:
                return letter_grade
        return "F"

    def recalculate(
        self,
        max_possible_marks: float,
        subject_ids: Optional[Sequence[str]] = None
    ) -> None:
        """Recalculate and update percentage and grade using the configured maximum marks."""
        self._percentage = self.calculate_percentage(max_possible_marks, subject_ids)
        self._grade = self.calculate_grade(self._percentage)

    def get_mark(self, subject_id: str, fallback_name: Optional[str] = None) -> Optional[float]:
        """
        Retrieve mark by subject ID, with optional fallback by subject name
        for backward compatibility with unmigrated in-memory structures.
        """
        if subject_id in self._marks:
            return self._marks[subject_id]
        if fallback_name and fallback_name in self._marks:
            return self._marks[fallback_name]
        return None

    def get_details(self) -> Dict[str, Any]:
        """Override Person.get_details() to include academic data."""
        details = super().get_details()
        details.update({
            "student_id": self._student_id,
            "class_div": self._class_div,
            "marks": self._marks,
            "total_marks": self.calculate_total_marks(),
            "percentage": self._percentage,
            "grade": self._grade
        })
        return details

    def to_dict(self) -> Dict[str, Any]:
        """Serialize student data to dictionary for JSON storage."""
        return {
            "student_id": self._student_id,
            "name": self._name,
            "class_div": self._class_div,
            "marks": self._marks,
            "percentage": self._percentage,
            "grade": self._grade
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        max_possible_marks: Optional[float] = None
    ) -> "Student":
        """Instantiate Student from dictionary."""
        return cls(
            student_id=data.get("student_id", ""),
            name=data.get("name", ""),
            class_div=data.get("class_div", ""),
            marks=data.get("marks", {}),
            percentage=data.get("percentage"),
            grade=data.get("grade"),
            max_possible_marks=max_possible_marks
        )

    def __str__(self) -> str:
        return f"Student(ID={self._student_id}, Name='{self._name}', Grade='{self._grade}')"
