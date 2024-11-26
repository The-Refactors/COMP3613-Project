from App.database import db

class Student(db.Model):
  #__tablename__ = 'student'
  #id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  id = db.Column(db.Integer, primary_key=True)
  studentid = db.Column(db.String(10), nullable=False)
  reviews = db.relationship('Review', backref='studentReviews', lazy='joined')
  karma = db.Column(db.Integer, nullable=True)

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

  def __init__(self, studentid):

    self.studentid=studentid

  def get_id(self):
    return self.id

  def get_json(self):
    return{
        'id': self.id,
        'studentid': self.studentid,
    }

  def __repr__(self):
    return f'<Student {self.studentid}>'
