import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Staff
from App.controllers import (
    create_staff,
    login,
    get_staff_by_id,
    get_staff_by_name,
    get_staff_by_username,
    get_all_staff_json,
    get_review
)
'''
   Unit Tests
'''
class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
         staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass")
         assert staff.username == "joe"

    def test_get_json(self):
         staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass")
         staff_json = staff.get_json()
         print(staff_json)
         self.assertDictEqual(staff_json, {
             "id": None,
             "username": "joe",
             "firstname": "Joe",
             "lastname": "Mama",
             "email": "joe@example.com",
             "user_type": "staff"
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

class StaffIntegrationTests(unittest.TestCase):



    def test_create_staff(self):
        staff = create_staff(username="rick",firstname="Rick", lastname="Grimes", email="rick@example.com", password="rickpass")
        assert staff.username == "rick"

    def test_authenticate(self):
        user = create_staff(username="bob", firstname="Bob", lastname="Smith", email="bob@example.com", password="bobpass")
        assert login("bob", "bobpass") != None
    

    def test_get_staff_by_id(self):
        staff = get_staff_by_id(1)
        assert staff is not None

    def test_get_staff_by_name(self):
        staff = get_staff_by_name("Rick", "Grimes")
        assert staff is not None

    def test_get_staff_by_username(self):
        staff = get_staff_by_username("rick")
        assert staff is not None

    def test_get_all_staff_json(self):
        staff_json = get_all_staff_json()
        self.assertListEqual([{"id":1, 
            "username":"bob", 
            "firstname":"Bob", 
            "lastname":"Smith", 
            "email":"bob@example.com",
            "user_type": "staff"},
            {
            "id":2, 
            "username":"rick", 
            "firstname":"Rick", 
            "lastname":"Grimes", 
            "email":"rick@example.com",
            "user_type": "staff"
            }], staff_json)


    # def test_get_staff_by_username(self):
    #     staff = get_staff_by_username("joe")
    #     assert staff is not None

    # def test_staff_create_review(self):
    #     assert create_student(username="billy",
    #              firstname="Billy",
    #              lastname="John",
    #              email="billy@example.com",
    #              password="billypass",
    #              faculty="FST",
    #              admittedTerm="",
    #              UniId='816031160',
    #              degree="",
    #              gpa="") == True
    #     student = get_student_by_username("billy")
    #     staff = get_staff_by_id(1)
    #     assert staff is not None
    #     assert staff_create_review(staff, student, True, 3, "Billy is good.") == True

    # def test_staff_edit_review(self):
    #     review = get_review(1)
    #     assert review is not None
    #     assert staff_edit_review(review.id, "Billy is very good") == True