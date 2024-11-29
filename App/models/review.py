from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from App.database import db
from .student import Student
from datetime import datetime


class Review(db.Model):
  __tablename__ = 'review'
  id = db.Column(db.Integer, primary_key=True)
  student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
  staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
  #isPositive = db.Column(db.Boolean, nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  points = db.Column(db.Integer, nullable=False)
  details = db.Column(db.String(400), nullable=False)
  #student = db.relationship('Student', backref='reviews', lazy='joined')
  # studentSeen = db.Column(db.Boolean, nullable=False, default=False)

  #def __init__(self, staff, student, isPositive, points, details):
  def __init__(self, staff, student, points, details):
    #self.createdByStaffID = staff.id
    self.staff_id = staff.id
    # self.student= student
    self.student_id = student.id
    #self.isPositive = isPositive
    self.points = points
    self.details = details
    self.date_created = datetime.now()

  __table_args__ = (
      CheckConstraint("points IN (-3, -2, -1, 1, 2, 3)", name='check_points'),
  )

  @validates('points')
  def validate_points(self, key, points):
    try:
      points = int(points)
    except TypeError:
      raise TypeError("Points must be an integer")
    if points not in [-3, -2, -1, 1, 2, 3]:
      raise ValueError("Points must be -3, -2, -1, 1, 2 or 3")
    return points


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
        "review_id": self.id,
        "reviewer": staff.firstname + " " + staff.lastname,
        "student_id": student.id,
        #"studentName": student.firstname + " " + student.lastname,
        "created":
        self.date_created.strftime("%d-%m-%Y %H:%M"),  #format the date/time
        #"isPositive": self.isPositive,
        "points": self.points,
        "details": self.details,
    }

    def __repr__(self):
      return f'<Review - Staff: {self.staff_id}, Student: {self.student_id}, Details: {self.details}>'
