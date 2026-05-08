from student import Student


class Gradebook:
    def __init__(self):
        self._students: dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        self._students[student.student_id] = student

    def remove_student(self, student_id: str) -> bool:
        if student_id in self._students:
            del self._students[student_id]
            return True
        return False

    def find_by_name(self, name: str) -> list[Student]:
        return [s for s in self._students.values() if s.name.lower() == name.lower()]

    def top_students(self, n: int = 3) -> list[Student]:
        sorted_students = sorted(
            self._students.values(),
            key=lambda s: s.get_average(),
            reverse=True,
        )
        return sorted_students[:n]

    def class_average(self) -> float:
        students = list(self._students.values())
        if not students:
            return 0.0
        return sum(s.get_average() for s in students) / len(students)

    def __len__(self) -> int:
        return len(self._students)
