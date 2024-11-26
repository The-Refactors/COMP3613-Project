from App.database import db
from .student import Student
from datetime import datetime


class Review(db.Model):
  __tablename__ = 'review'
  ID = db.Column(db.Integer, primary_key=True)
  studentID = db.Column(db.Integer, db.ForeignKey('student.ID'))
  staffID = db.Column(db.Integer, db.ForeignKey('staff.ID'))
  #isPositive = db.Column(db.Boolean, nullable=False)
  dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
  points = db.Column(db.Integer, nullable=False)
  details = db.Column(db.String(400), nullable=False)
  #student = db.relationship('Student', backref='reviews', lazy='joined')
  # studentSeen = db.Column(db.Boolean, nullable=False, default=False)

  #def __init__(self, staff, student, isPositive, points, details):
  def __init__(self, staff, student, points, details):
    #self.createdByStaffID = staff.ID
    self.staffID = staff.ID
    # self.student= student
    self.studentID = student.ID
    #self.isPositive = isPositive
    self.points = points
    self.details = details
    self.dateCreated = datetime.now()


  def get_id(self):
    return self.ID

  # def deleteReview(self, staff):
  #   if self.reviewer == staff:
  #     db.session.delete(self)
  #     db.session.commit()
  #     return True
  #   return None

  def get_json(self, student, staff):
    return {
        "reviewID": self.ID,
        "reviewer": staff.firstname + " " + staff.lastname,
        "studentID": student.ID,
        #"studentName": student.firstname + " " + student.lastname,
        "created":
        self.dateCreated.strftime("%d-%m-%Y %H:%M"),  #format the date/time
        #"isPositive": self.isPositive,
        "points": self.points,
        "details": self.details,
    }

    def __repr__(self):
      return f'<Review - Staff: {self.staffID}, Student: {self.studentID}, Is Positive: {self.isPositive}, Details: {self.details}>'
