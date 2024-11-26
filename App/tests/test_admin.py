import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Admin
from App.controllers import (
    add_staff,
    add_student,
    admin_update_name,
    admin_update_username,
    admin_update_email,
    admin_update_password,
    get_student_by_username
)
'''
   Unit Tests
'''
class AdminUnitTests(unittest.TestCase):
    
    def test_new_admin(self):
        newAdmin = Admin(username="phil",firstname="Phil", lastname="Smith", email="phil@example.com", password="philpass")
        assert newAdmin.username == "phil"
    
    def test_to_json(self):
        newAdmin = Admin(username="phil",firstname="Phil", lastname="Smith", email="phil@example.com", password="philpass")
        newAdmin_json = newAdmin.to_json()
        self.assertDictEqual(newAdmin_json,{
            "adminID": None,
            "username": "phil",
            "firstname": "Phil",
            "lastname": "Smith",
            "email": "phil@example.com"
        })

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class AdminIntegrationTests(unittest.TestCase):

    def test_add_teacher(self):
        assert add_staff(username="john", firstname="John", lastname="Doe", email="john@example.com", password="johnpassword") == True
        

    def test_add_student(self):
        assert add_student(studentID) == True
       

    # def test_admin_update_name(self):
    #     self.test_add_student()
    #     student = get_student_by_username("alice")
    #     assert admin_update_name(student.id, "NewFirstName", "NewLastName") == True
       

    # def test_admin_update_username(self):
    #     self.test_add_student()
    #     staff = get_student_by_username("alice")
    #     assert admin_update_username(student.id, "newusername") == True
        

    # def test_admin_update_email(self):
    #     self.test_add_student()
    #     student = get_student_by_username("alice")
    #     assert admin_update_email(student.id, "newemail@example.com") == True

    # def test_admin_update_password(self):
    #     self.test_add_student()
    #     student = get_student_by_username("alice")
    #     assert admin_update_password(student.id, "newpassword") == True

    # def test_admin_update_faculty(self):
    #     self.test_add_student()
    #     student = get_student_by_username("alice")
    #     assert admin_update_faculty(student.id, "FSS") == True

    # def test_admin_update_student_admittedTerm(self):
    #     self.test_add_student()
    #     student = get_student_by_username("alice")
    #     assert admin_update_student_admittedTerm(student.id, "2023/2024") == True
        

    # def test_admin_update_student_yearOfStudy(self):
    #     self.test_add_student()
    #     student = get_student_by_username("alice")
    #     assert admin_update_student_yearOfStudy(student.id, 2) == True
        

    # def test_admin_update_student_degree(self):
    #     self.test_add_student()
    #     student = get_student_by_username("alice")
    #     assert admin_update_student_degree(student.id, "MSc Computer Science") == True
        
