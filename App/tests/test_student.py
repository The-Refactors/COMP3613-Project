import os, tempfile, pytest, logging, unittest
from App.main import create_app
from App.database import db, create_db
from App.models import Student
from App.controllers import (
    create_student,
    get_student_by_id,
    get_student_by_student_id,
    get_all_students_json,
)

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        student = Student(student_id="816000000")
        assert student.student_id == "816000000"

    def test_get_json(self):
        student = Student(student_id="816000000")
        student.set_karma(0.0)
        student_json = student.get_json()
        self.assertDictEqual(student_json, {
            "id": 1,
            "system_id": None,
            "karma": 0.0,
            "karmarank": None,
            "studentid": "816000000",
            "reviews": 0
        })


'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        student = create_student(student_id="816000001", system_id="SYS001")
        assert student.student_id == "816000001"
        
    def test_get_student_by_id(self):
        student = create_student(student_id="816000002", system_id="SYS002")
        fetched_student = get_student_by_id(student.id)
        assert fetched_student.student_id == "816000002"

    def test_get_student_by_student_id(self):
        create_student(student_id="816000003", system_id="SYS003")
        student = get_student_by_student_id("816000003")
        assert student is not None
        assert student.student_id == "816000003"

    def test_get_all_students_json(self):
        create_student(student_id="816000004", system_id="SYS004")
        create_student(student_id="816000005", system_id="SYS005")
        students_json = get_all_students_json()
        assert len(students_json) >= 2
        assert any(student['studentid'] == "816000004" for student in students_json)
        assert any(student['studentid'] == "816000005" for student in students_json)
