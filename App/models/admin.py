from App.database import db
from .user import User


class Admin(User):
  __tablename__ = 'admin'
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

  __mapper_args__ = {"polymorphic_identity": "admin"}

  def __init__(self, username, firstname, lastname, password, email):
    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     password=password,
                     email=email)
