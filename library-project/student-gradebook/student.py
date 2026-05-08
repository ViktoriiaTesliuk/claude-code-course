"""Module containing the Student data model for the gradebook system."""


class Student:
    """Represents a single student with a name, ID, and grade records.

    Attributes:
        name: The full name of the student.
        student_id: A unique identifier string for the student.
        grades: A mapping of subject names to numeric grades (0–100).
    """

    def __init__(self, name: str, student_id: str) -> None:
        """Initialise a new Student.

        Args:
            name: The student's full name. Must be a non-empty string.
            student_id: A unique identifier for the student.
                Must be a non-empty string.

        Raises:
            TypeError: If ``name`` or ``student_id`` is not a string.
            ValueError: If ``name`` or ``student_id`` is empty or whitespace-only.
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be a str, got {type(name).__name__}")
        if not name.strip():
            raise ValueError("name must not be empty")
        if not isinstance(student_id, str):
            raise TypeError(f"student_id must be a str, got {type(student_id).__name__}")
        if not student_id.strip():
            raise ValueError("student_id must not be empty")

        self.name = name
        self.student_id = student_id
        self.grades: dict[str, float] = {}

    def add_grade(self, subject: str, grade: float) -> None:
        """Record or overwrite a grade for a subject.

        Args:
            subject: The name of the subject. Must be a non-empty string.
            grade: The numeric grade. Must be an int or float in the
                inclusive range 0–100. Booleans are not accepted.

        Raises:
            TypeError: If ``subject`` is not a string, or if ``grade``
                is not an int or float (booleans are rejected).
            ValueError: If ``subject`` is empty or whitespace-only, or if
                ``grade`` is outside the range 0–100.
        """
        if not isinstance(subject, str):
            raise TypeError(f"subject must be a str, got {type(subject).__name__}")
        if not subject.strip():
            raise ValueError("subject must not be empty")
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise TypeError(f"grade must be a number, got {type(grade).__name__}")
        if not (0 <= grade <= 100):
            raise ValueError(f"grade must be between 0 and 100 inclusive, got {grade}")

        self.grades[subject] = float(grade)

    def get_average(self) -> float:
        """Calculate the mean of all recorded grades.

        Returns:
            The arithmetic mean of all grades, or 0.0 if no grades
            have been recorded yet.
        """
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def get_highest(self) -> tuple[str, float] | None:
        """Find the subject with the highest grade.

        Returns:
            A (subject, grade) tuple for the top-scoring subject,
            or None if no grades have been recorded.
        """
        if not self.grades:
            return None
        subject = max(self.grades, key=lambda s: self.grades[s])
        return subject, self.grades[subject]

    def get_lowest(self) -> tuple[str, float] | None:
        """Find the subject with the lowest grade.

        Returns:
            A (subject, grade) tuple for the lowest-scoring subject,
            or None if no grades have been recorded.
        """
        if not self.grades:
            return None
        subject = min(self.grades, key=lambda s: self.grades[s])
        return subject, self.grades[subject]

    def __str__(self) -> str:
        """Return a human-readable summary of the student.

        Returns:
            A string in the format "Student(<id>): <name>, average: <avg>".
        """
        avg = self.get_average()
        return f"Student({self.student_id}): {self.name}, average: {avg:.2f}"
