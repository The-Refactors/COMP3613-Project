from App.database import db
from .user import User

class Staff(User):
  __tablename__ = 'staff'
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  reviews = db.relationship('Review', backref='staff_reviews', lazy='joined')

  __mapper_args__ = {"polymorphic_identity": "staff"}

  def __init__(self, username, firstname, lastname, email, password):
    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     email=email,
                     password=password)
    self.reviews = []

