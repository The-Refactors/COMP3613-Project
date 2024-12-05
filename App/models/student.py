from App.database import db
from .karmaObserver import KarmaObserver

class Student(KarmaObserver):
  __tablename__ = 'student'
  id = db.Column(db.Integer, db.ForeignKey('karma_observer.id'), primary_key=True)
  student_id = db.Column(db.String(10), nullable=False, unique=True)
  reviews = db.relationship('Review', backref='student', lazy='joined', cascade='all, delete-orphan')

  __mapper_args__ = {"polymorphic_identity": "student"}

  def __init__(self, student_id):

    self.student_id=student_id

  def get_id(self):
    return self.id

  def get_json(self):
    return{
        'id': self.id,
        'system_id': self.system_id,
        'karma': float(self.karma),
        'karmarank': self.karma_rank,
        'studentid': self.student_id,
        'reviews': len(self.reviews)
    }

  def __repr__(self):
    return f'<Id: {self.id}, SystemId: {self.system_id}, Karma: {float(self.karma)}, KarmaRank: {self.karma_rank}, StudentId: {self.student_id}, Reviews: {len(self.reviews)}>'
