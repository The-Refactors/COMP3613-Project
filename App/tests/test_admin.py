import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Admin
from App.controllers import (
    create_admin,
    get_all_admins,
    get_all_admins_json,
    login
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
        newAdmin_json = newAdmin.get_json()
        self.assertDictEqual(newAdmin_json,{
            "id": None,
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



    def test_create_admin(self):
        user = create_admin("rick", "Rick", "Grimes", "rick@example.com" , "rickpass")
        assert user.username == "rick"

    def test_authenticate(self):
        user = create_admin("bob", "Bob", "Smith", "bob@example.com", "bobpass")
        assert login("bob", "bobpass") != None

    def test_get_all_admins_json(self):
        admins_json = get_all_admins_json()
        self.assertListEqual([{"id":1, 
            "username":"bob", 
            "firstname":"Bob", 
            "lastname":"Smith", 
            "email":"bob@example.com"},
            {
            "id":2, 
            "username":"rick", 
            "firstname":"Rick", 
            "lastname":"Grimes", 
            "email":"rick@example.com", 
            }], admins_json)
