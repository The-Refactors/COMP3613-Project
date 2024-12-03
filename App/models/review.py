from datetime import datetime

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from App.database import db


class Review(db.Model):
  __tablename__ = 'review'
  id = db.Column(db.Integer, primary_key=True)
  student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
  staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
  points = db.Column(db.Integer, nullable=False)
  details = db.Column(db.String(400), nullable=False)

  def __init__(self, staff, student, points, details, date_created=datetime.now()):
    self.staff_id = staff.id
    self.student_id = student.id
    self.points = points
    self.details = details
    #self.date_created = datetime.now()
    self.date_created = date_created

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
        "created": self.date_created.strftime("%d-%m-%Y %H:%M"),  #format the date/time
        "points": self.points,
        "details": self.details
    }

  def __repr__(self):
    return f'<ReviewId: {self.id}, StaffId: {self.staff_id}, StudentId: {self.student_id}, Date: {self.date_created}, Points: {self.points}, Details: {self.details}>'
