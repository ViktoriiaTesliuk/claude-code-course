"""Module containing the Gradebook data model for the gradebook system."""

from student import Student


class Gradebook:
    """Manages a collection of students and provides aggregate queries.

    Students are keyed internally by their ``student_id``. All mutation
    methods validate their inputs and raise standard Python exceptions on
    invalid data.
    """

    def __init__(self) -> None:
        """Initialise an empty gradebook."""
        self._students: dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        """Add a student to the gradebook.

        Args:
            student: The Student instance to add.

        Raises:
            TypeError: If ``student`` is not a Student instance.
            KeyError: If a student with the same ``student_id`` already
                exists in the gradebook.
        """
        if not isinstance(student, Student):
            raise TypeError(f"student must be a Student instance, got {type(student).__name__}")
        if student.student_id in self._students:
            raise KeyError(f"A student with id '{student.student_id}' already exists")
        self._students[student.student_id] = student

    def remove_student(self, student_id: str) -> bool:
        """Remove a student by their ID.

        Args:
            student_id: The unique ID of the student to remove.
                Must be a non-empty string.

        Returns:
            True if the student was found and removed,
            False if no student with that ID exists.

        Raises:
            TypeError: If ``student_id`` is not a string.
            ValueError: If ``student_id`` is empty or whitespace-only.
        """
        if not isinstance(student_id, str):
            raise TypeError(f"student_id must be a str, got {type(student_id).__name__}")
        if not student_id.strip():
            raise ValueError("student_id must not be empty")

        if student_id in self._students:
            del self._students[student_id]
            return True
        return False

    def find_by_name(self, name: str) -> list[Student]:
        """Return all students whose name matches (case-insensitive).

        Args:
            name: The full name to search for. Must be a non-empty string.

        Returns:
            A list of matching Student objects (may be empty).

        Raises:
            TypeError: If ``name`` is not a string.
            ValueError: If ``name`` is empty or whitespace-only.
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be a str, got {type(name).__name__}")
        if not name.strip():
            raise ValueError("name must not be empty")

        return [s for s in self._students.values() if s.name.lower() == name.lower()]

    def top_students(self, n: int = 3) -> list[Student]:
        """Return the top-n students ranked by grade average.

        Args:
            n: The maximum number of students to return. Must be a positive
                integer greater than 0. Booleans are not accepted.
                Defaults to 3.

        Returns:
            A list of up to n Student objects sorted by descending average.
            If the gradebook has fewer than n students, the full roster
            is returned.

        Raises:
            TypeError: If ``n`` is not an integer (booleans are rejected).
            ValueError: If ``n`` is less than or equal to 0.
        """
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError(f"n must be an int, got {type(n).__name__}")
        if n <= 0:
            raise ValueError(f"n must be a positive integer, got {n}")

        sorted_students = sorted(
            self._students.values(),
            key=lambda s: s.get_average(),
            reverse=True,
        )
        return sorted_students[:n]

    def class_average(self) -> float:
        """Calculate the mean of all students' individual averages.

        Returns:
            The arithmetic mean of each student's get_average(),
            or 0.0 if the gradebook is empty.
        """
        students = list(self._students.values())
        if not students:
            return 0.0
        return sum(s.get_average() for s in students) / len(students)

    def __len__(self) -> int:
        """Return the number of students currently in the gradebook.

        Returns:
            Integer count of enrolled students.
        """
        return len(self._students)
