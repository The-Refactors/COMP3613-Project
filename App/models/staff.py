from App.database import db
from .user import User

class Staff(User):
  __tablename__ = 'staff'
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  reviews = db.relationship('Review', backref='staff', lazy='joined', cascade='all, delete-orphan')

  __mapper_args__ = {"polymorphic_identity": "staff"}

  def __init__(self, username, firstname, lastname, password, email):
    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     password=password,
                     email=email)
    self.reviews = []

