"""Subject model representing an academic subject with dynamic configuration."""

from typing import Dict, Any


class Subject:
    """Class representing an academic subject with stable ID, name, and maximum marks."""

    def __init__(self, subject_id: str, name: str, max_marks: float = 100.0):
        self._id: str = str(subject_id).strip()
        self._name: str = str(name).strip()
        self._max_marks: float = float(max_marks)

    @property
    def id(self) -> str:
        """Unique, stable subject identifier (e.g., SUB01)."""
        return self._id

    @property
    def name(self) -> str:
        """Subject display name (e.g., 'Advanced Python')."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        cleaned = str(value).strip()
        if not cleaned:
            raise ValueError("Subject name cannot be empty.")
        self._name = cleaned

    @property
    def max_marks(self) -> float:
        """Maximum possible marks for this subject (e.g., 100.0, 50.0)."""
        return self._max_marks

    @max_marks.setter
    def max_marks(self, value: float) -> None:
        val = float(value)
        if val <= 0:
            raise ValueError("Maximum marks must be a positive number greater than 0.")
        self._max_marks = round(val, 2)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize subject data to dictionary for JSON persistence."""
        return {
            "id": self._id,
            "name": self._name,
            "max_marks": self._max_marks,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Subject":
        """Instantiate Subject from dictionary."""
        return cls(
            subject_id=data.get("id", ""),
            name=data.get("name", ""),
            max_marks=float(data.get("max_marks", 100.0))
        )

    def __str__(self) -> str:
        return f"Subject(id='{self._id}', name='{self._name}', max_marks={self._max_marks})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Subject):
            return self._id == other._id
        return False
