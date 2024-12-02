import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_username,
    update_email,
    update_faculty,
    update_name,
    update_password
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
         user = User(username="bob", firstname="Bob", lastname="Smith", password="bobpass", email="bob@example.com")
         assert user.username == "bob"

    def test_get_json(self):
         user = User(username="bob", firstname="Bob", lastname="Smith", password="bobpass", email="bob@example.com")
         user_json = user.get_json()
         self.assertDictEqual(user_json, {"id":None, "username":"bob", "firstname":"Bob", "lastname":"Smith", "email":"bob@example.com"})

    def test_hashed_password(self):
         password = "mypass"
         hashed = generate_password_hash(password, method='sha256')
         user = User(username="bob", firstname="Bob", lastname="Smith", password=password, email="bob@example.com")
         assert user.password != password

    def test_check_password(self):
         password = "mypass"
         user = User(username="bob", firstname="Bob", lastname="Smith", password=password, email="bob@example.com")
         assert user.check_password(password)

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


class UserIntegrationTests(unittest.TestCase):

    def test_authenticate(self):
        user = create_user("bob", "Bob", "Smith", "bobpass", "bob@example.com")
        assert login("bob", "bobpass") != None

    def test_create_user(self):
        user = create_user("rick", "Rick", "Grimes", "rickpass", "rick@example.com")
        assert user.username == "rick"


    def test_get_all_users_json(self):
        users_json = get_all_users_json()
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
            }], users_json)

    # # Tests data changes in the database
    # def test_update_user(self):
    #     update_username(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username == "ronnie"

    # def test_update_name(self):
    #     update_name(1, "Bobby", "Jones")
    #     user = get_user(1)
    #     assert user.firstname == "Bobby"
    #     assert user.lastname == "Jones"

    # def test_update_email(self):
    #     update_email(1, "newemail@example.com")
    #     user = get_user(1)
    #     assert user.email == "newemail@example.com"

    # def test_update_password(self):
    #     update_password(1, "newpass")
    #     user = get_user(1)
    #     assert user.check_password("newpass")

    # def test_update_faculty(self):
    #     update_faculty(1, "New Faculty")
    #     user = get_user(1)
    #     assert user.faculty == "New Faculty"