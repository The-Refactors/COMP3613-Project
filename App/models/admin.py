from App.database import db
from .user import User


class Admin(User):
  __tablename__ = 'admin'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)

  __mapper_args__ = {"polymorphic_identity": "admin"}

  def __init__(self, username, firstname, lastname, email, password):
    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     email=email,
                     password=password)


#return admin details on json format

  def get_json(self):
    return {
        "adminID": self.ID,
        "username": self.username,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email
    }

  def __repr__(self):
    return f'<Admin {self.ID} :{self.email}>'
