import pytest
from App.main import create_app
from App.database import db
from App.models.staff import Staff
from App.models.admin import Admin
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="module")
def test_client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def setup_users():
    staff = Staff(
        username="unique_staff_user",
        firstname="John",
        lastname="Doe",
        email="staff@example.com",
        password=generate_password_hash("password123")
    )
    db.session.add(staff)
    db.session.commit()

    # Debugging: Confirm the user is added
    user = Staff.query.filter_by(username="unique_staff_user").first()
    print(f"Added staff user: {user}")  # Debug log


def test_login_success_staff(test_client, setup_users):
    payload = {"username": "unique_staff_user", "password": "password123"}
    response = test_client.post('/login', json=payload)
    assert response.status_code == 200
    data = response.json
    assert data["message"] == "Login successful"
    assert data["user"]["username"] == "unique_staff_user"

""" 
def test_login_success_admin(test_client, setup_users):
    payload = {"username": "adminuser", "password": "admin123"}
    response = test_client.post('/login', json=payload)
    assert response.status_code == 200
    data = response.json
    assert data["message"] == "Login successful"
    assert data["user"]["role"] == "Admin"

def test_login_invalid_username(test_client):
    payload = {"username": "invaliduser", "password": "password123"}
    response = test_client.post('/login', json=payload)
    assert response.status_code == 401
    data = response.json
    assert data["error"] == "Invalid username or password"

def test_login_invalid_password(test_client, setup_users):
    payload = {"username": "staffuser", "password": "wrongpassword"}
    response = test_client.post('/login', json=payload)
    assert response.status_code == 401
    data = response.json
    assert data["error"] == "Invalid username or password"

def test_login_missing_fields(test_client):
    payload = {"username": "staffuser"}
    response = test_client.post('/login', json=payload)
    assert response.status_code == 400
    data = response.json
    assert data["error"] == "Username and password are required"



"""