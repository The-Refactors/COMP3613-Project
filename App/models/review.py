from App.database import db
from .student import Student
from datetime import datetime


class Review(db.Model):
  __tablename__ = 'review'
  id = db.Column(db.Integer, primary_key=True)
  studentid = db.Column(db.Integer, db.ForeignKey('student.id'))
  staffid = db.Column(db.Integer, db.ForeignKey('staff.id'))
  #isPositive = db.Column(db.Boolean, nullable=False)
  datecreated = db.Column(db.DateTime, default=datetime.utcnow)
  points = db.Column(db.Integer, nullable=False)
  details = db.Column(db.String(400), nullable=False)
  #student = db.relationship('Student', backref='reviews', lazy='joined')
  # studentSeen = db.Column(db.Boolean, nullable=False, default=False)

  #def __init__(self, staff, student, isPositive, points, details):
  def __init__(self, staff, student, points, details):
    #self.createdByStaffID = staff.id
    self.staffid = staff.id
    # self.student= student
    self.studentid = student.id
    #self.isPositive = isPositive
    self.points = points
    self.details = details
    self.datecreated = datetime.now()


  def get_id(self):
    return self.id

  # def deleteReview(self, staff):
  #   if self.reviewer == staff:
  #     db.session.delete(self)
  #     db.session.commit()
  #     return True
  #   return None

  def get_json(self, student, staff):
    return {
        "reviewID": self.id,
        "reviewer": staff.firstname + " " + staff.lastname,
        "studentid": student.id,
        #"studentName": student.firstname + " " + student.lastname,
        "created":
        self.datecreated.strftime("%d-%m-%Y %H:%M"),  #format the date/time
        #"isPositive": self.isPositive,
        "points": self.points,
        "details": self.details,
    }

    def __repr__(self):
      return f'<Review - Staff: {self.staffid}, Student: {self.studentid}, Details: {self.details}>'
