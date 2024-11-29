from App.database import db
from .karmaObserver import KarmaObserver

class Student(KarmaObserver):
  __tablename__ = 'student'
  id = db.Column(db.Integer, db.ForeignKey('karma_observer.id'), primary_key=True)
  student_id = db.Column(db.String(10), nullable=False, unique=True)
  reviews = db.relationship('Review', backref='student_reviews', lazy='joined')

  __mapper_args__ = {"polymorphic_identity": "student"}

  # degree = db.Column(db.String(120), nullable=False)
  # fullname = db.Column(db.String(255), nullable=True)
  # degree = db.Column(db.String(120), nullable=False)
  # admittedTerm = db.Column(db.String(120), nullable=False)
  # #yearOfStudy = db.Column(db.Integer, nullable=False)
  # gpa = db.Column(db.String(120), nullable=True)

  # accomplishments = db.relationship('Accomplishment',
  #                                   backref='studentAccomplishments',
  #                                   lazy='joined')
  # incidents = db.relationship('IncidentReport',
  #                             backref='studentincidents',
  #                             lazy='joined')
  # grades = db.relationship('Grades', backref='studentGrades', lazy='joined')
  # transcripts = db.relationship('Transcript', backref='student', lazy='joined')
  # badges = db.relationship('Badges', backref='studentbadge', lazy='joined')

  # karmaID = db.Column(db.Integer, db.ForeignKey('karma.karmaID'))

  # __mapper_args__ = {"polymorphic_identity": "student"}

  def __init__(self, student_id):

    self.student_id=student_id

  def get_id(self):
    return self.id

  def get_json(self):
    return{
        'id': self.id,
        'studentid': self.student_id,
    }

  def __repr__(self):
    return f'<Student {self.student_id}>'
