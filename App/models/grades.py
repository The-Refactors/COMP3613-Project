from App.database import db
from .student import Student

class Grades(db.Model):
  # __tablename__ = 'Grades'
  # id = db.Column(db.Integer , primary_key=True)
  # studentid = db.Column(db.Integer, db.ForeignKey('student.id'))
  # course = db.Column(db.String(120), nullable=False)
  # grade = db.Column(db.String(120), nullable=False)

  # def __init__(self, studentid ,course, grade):
  #   self.course = course
  #   self.grade = grade
  #   self.studentid = studentid

  # def to_json(self):
  #   return {
  #       "id": self.id,
  #       "studentid": self.studentid,
  #       "course": self.course,
  #       "grade": self.grade
  #   }