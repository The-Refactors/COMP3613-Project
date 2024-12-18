from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from App.database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type,
    }

    def __init__(self, username, firstname, lastname, email, password):
        self.username= username
        self.firstname = firstname
        self.lastname = lastname
        self.set_password(password)
        self.email = email

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'user_type': self.user_type
        }
    
    def get_id(self):
        return self.id

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Id: {self.id}, Username: {self.username}, Name: {self.firstname} {self.lastname}, Email: {self.email}, Type: {self.user_type}>'