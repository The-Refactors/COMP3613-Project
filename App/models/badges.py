from App.database import db


class Badges(db.Model):
  # __tablename__ = "badges"
  # id = db.Column(db.Integer, primary_key=True)
  # studentid = db.Column(db.Integer, db.ForeignKey('student.id'))
  # name = db.Column(db.String(40), nullable=False)
  # details = db.Column(db.String(40), nullable=False)
  # imageLink = db.Column(db.String(400), nullable=False)
  # studentSeen = db.Column(db.Boolean, nullable=False, default=False)

  # def __init__(self, student, name, details, imageLink, studentSeen):
  #   self.studentid = student.id
  #   self.name = name
  #   self.details = details
  #   self.imageLink = imageLink
  #   self.studentSeen = studentSeen
