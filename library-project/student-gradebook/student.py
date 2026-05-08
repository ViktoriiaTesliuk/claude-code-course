class Student:
    def __init__(self, name: str, student_id: str):
        self.name = name
        self.student_id = student_id
        self.grades: dict[str, float] = {}

    def add_grade(self, subject: str, grade: float) -> None:
        self.grades[subject] = grade

    def get_average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def get_highest(self) -> tuple[str, float] | None:
        if not self.grades:
            return None
        subject = max(self.grades, key=lambda s: self.grades[s])
        return subject, self.grades[subject]

    def get_lowest(self) -> tuple[str, float] | None:
        if not self.grades:
            return None
        subject = min(self.grades, key=lambda s: self.grades[s])
        return subject, self.grades[subject]

    def __str__(self) -> str:
        avg = self.get_average()
        return f"Student({self.student_id}): {self.name}, average: {avg:.2f}"
