from App.database import db
from App.models import Student, Review

def create_student(student_id, system_id):
    existing_student = get_student_by_student_id(student_id)
    if existing_student:
        print("[student.create_student] Student already exists.")
        return existing_student

    new_student = Student(student_id=student_id)
    db.session.add(new_student)
    new_student.observe_system(system_id)
    try:
        db.session.commit()
        return new_student
    except Exception as e:
        print("[student.create_student] Error occurred while creating new student: ", str(e))
        db.session.rollback()
        return False


def get_student_by_id(id):
  student = Student.query.filter_by(id=id).first()
  if student:
    return student
  else:
    return None


def get_student_by_student_id(student_id):
  student = Student.query.filter_by(student_id=student_id).first()
  if student:
    return student
  else:
    return None

def get_student_by_student_id_json(student_id):
  student = Student.query.filter_by(student_id=student_id).first().get_json()
  if student:
    return student
  else:
    return None


def get_students_by_ids(student_ids):
  students = Student.query.filter(Student.id.in_(student_ids)).all()
  return students

def get_karma_ordered_students_by_system_id(system_id):
  students = Student.query.filter_by(system_id=system_id).order_by(Student.karma.desc()).all()
  return students

def get_all_students():
  students = Student.query.all()
  if not students:
    return None
  return students


def get_all_students_json():
  students = Student.query.all()
  if not students:
    return []
  return [student.get_json() for student in students]

def get_karma(student_id):
  student = Student.query.filter_by(student_id=student_id).first()
  if student:
    return student.karma
  return None
  
def get_karma_by_id(id):
  student = Student.get(id)
  if student:
    return student.karma
  return None

def delete_student(student_id):
  from .review import delete_review
  from .karmaSystem import update_karma, update_karma_ranking

  student = Student.query.filter_by(student_id=student_id).first()
  reviews = Review.query.filter_by(student_id=student.id).all()
  if student: 
    db.session.delete(student)

    for review in reviews:
      delete_review(review.id)

    try:
      db.session.commit()
      update_karma_ranking(1)
      return True
    except Exception as e:
      print("[student.delete_student] Error occurred while deleting student: ", str(e))
      db.session.rollback()
      return False
  else:
    return False


