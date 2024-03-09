from App.database import db
from .student import Student

class Admin(db.Model):
  __tablename__ = 'grades'
  ID = db.Column(db.String(10) , primary_key=True)
  studentID = db.Column(db.String(10), db.ForeignKey('student.ID'))
  course = db.Column(db.String(120), nullable=False)
  grade = db.Column(db.String(120), nullable=False)

  def __init__(self studentID ,course, grade):
    self.course = course
    self.grade = grade
    self.studentID = studentID

  def to_json(self):
    return {
        "ID": self.ID,
        "studentID": self.studentID,
        "course": self.course,
        "grade": self.grade
    }