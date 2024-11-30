from App.database import db
from .karmaObserver import KarmaObserver

class Student(KarmaObserver):
  __tablename__ = 'student'
  id = db.Column(db.Integer, db.ForeignKey('karma_observer.id'), primary_key=True)
  student_id = db.Column(db.String(10), nullable=False, unique=True)
  reviews = db.relationship('Review', backref='student_reviews', lazy='joined')

  __mapper_args__ = {"polymorphic_identity": "student"}

  def __init__(self, student_id):

    self.student_id=student_id

  def get_id(self):
    return self.id

  def get_json(self):
    return{
        'id': self.id,
        'studentid': self.student_id
    }

  def __repr__(self):
    return f'<Id: {self.id}, Student: {self.student_id}, Reviews: {self.reviews.count()}, Karma: {self.karma}, KarmaRank: {self.karma_rank}>'
