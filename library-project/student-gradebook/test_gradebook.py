import pytest
from student import Student
from gradebook import Gradebook


# ── Student ────────────────────────────────────────────────────────────────

class TestStudentInit:
    def test_attributes(self):
        s = Student("Alice", "S001")
        assert s.name == "Alice"
        assert s.student_id == "S001"
        assert s.grades == {}


class TestAddGrade:
    def test_adds_grade(self):
        s = Student("Alice", "S001")
        s.add_grade("Math", 90)
        assert s.grades["Math"] == 90

    def test_overwrites_existing(self):
        s = Student("Alice", "S001")
        s.add_grade("Math", 80)
        s.add_grade("Math", 95)
        assert s.grades["Math"] == 95


class TestGetAverage:
    def test_empty_grades(self):
        assert Student("Alice", "S001").get_average() == 0.0

    def test_single_grade(self):
        s = Student("Alice", "S001")
        s.add_grade("Math", 80)
        assert s.get_average() == 80.0

    def test_multiple_grades(self):
        s = Student("Alice", "S001")
        s.add_grade("Math", 80)
        s.add_grade("English", 90)
        s.add_grade("Science", 70)
        assert s.get_average() == pytest.approx(80.0)


class TestGetHighestLowest:
    def test_highest(self):
        s = Student("Alice", "S001")
        s.add_grade("Math", 95)
        s.add_grade("English", 70)
        assert s.get_highest() == ("Math", 95)

    def test_lowest(self):
        s = Student("Alice", "S001")
        s.add_grade("Math", 95)
        s.add_grade("English", 70)
        assert s.get_lowest() == ("English", 70)

    def test_returns_none_when_empty(self):
        s = Student("Alice", "S001")
        assert s.get_highest() is None
        assert s.get_lowest() is None


class TestStudentStr:
    def test_str_format(self):
        s = Student("Alice", "S001")
        s.add_grade("Math", 80)
        assert "Alice" in str(s)
        assert "S001" in str(s)
        assert "80.00" in str(s)


# ── Gradebook ──────────────────────────────────────────────────────────────

@pytest.fixture
def gradebook_with_students():
    gb = Gradebook()
    alice = Student("Alice", "S001")
    alice.add_grade("Math", 95)
    alice.add_grade("English", 85)

    bob = Student("Bob", "S002")
    bob.add_grade("Math", 70)
    bob.add_grade("English", 75)

    carol = Student("Carol", "S003")
    carol.add_grade("Math", 88)
    carol.add_grade("English", 92)

    gb.add_student(alice)
    gb.add_student(bob)
    gb.add_student(carol)
    return gb


class TestAddRemoveStudent:
    def test_add_increases_count(self):
        gb = Gradebook()
        gb.add_student(Student("Alice", "S001"))
        assert len(gb) == 1

    def test_remove_existing(self):
        gb = Gradebook()
        gb.add_student(Student("Alice", "S001"))
        assert gb.remove_student("S001") is True
        assert len(gb) == 0

    def test_remove_nonexistent(self):
        gb = Gradebook()
        assert gb.remove_student("S999") is False


class TestFindByName:
    def test_finds_match(self, gradebook_with_students):
        result = gradebook_with_students.find_by_name("Alice")
        assert len(result) == 1
        assert result[0].student_id == "S001"

    def test_case_insensitive(self, gradebook_with_students):
        assert len(gradebook_with_students.find_by_name("alice")) == 1

    def test_no_match(self, gradebook_with_students):
        assert gradebook_with_students.find_by_name("Zara") == []


class TestTopStudents:
    def test_returns_sorted_by_average(self, gradebook_with_students):
        top = gradebook_with_students.top_students(2)
        assert top[0].name == "Alice"
        assert top[1].name == "Carol"

    def test_n_larger_than_students(self, gradebook_with_students):
        assert len(gradebook_with_students.top_students(10)) == 3

    def test_empty_gradebook(self):
        assert Gradebook().top_students() == []


class TestClassAverage:
    def test_average(self, gradebook_with_students):
        # Alice: 90, Bob: 72.5, Carol: 90 → avg ≈ 84.17
        avg = gradebook_with_students.class_average()
        assert avg == pytest.approx(84.166, rel=1e-3)

    def test_empty_gradebook(self):
        assert Gradebook().class_average() == 0.0
