from App.database import db
from App.models import Staff
from .review import (
    get_review
)


def create_staff(username, firstname, lastname, password, email):
    new_staff = Staff(username,firstname, lastname, password, email)
    db.session.add(new_staff)
    
    try:
        db.session.commit()
        return new_staff
    except Exception as e:
        print("[staff.create_staff] Error occurred while creating new staff: ", str(e))
        db.session.rollback()
        return False
    

def get_staff_by_id(id):
    staff = Staff.query.filter_by(id=id).first()
    if staff:
        return staff
    else:
        return None

def get_staff_by_name(firstname, lastname):
  staff = Staff.query.filter_by(firstname=firstname, lastname=lastname).first()
  if staff:
      return staff
  else:
      return None

def get_staff_by_username(username):
    staff = Staff.query.filter_by(username=username).first()
    if staff:
        return staff
    else:
        return None

def staff_edit_review(id, details):
    review = get_review(id)
    if review is None:
        return False
    else:
        review.details = details
        db.session.add(review)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[staff.staff_edit_review] Error occurred while editing review:", str(e))
            db.session.rollback()
            return False


def get_all_staff():
    staff = Staff.query.all()
    if staff:
        return staff
    else:
        return None

def get_all_staff_json():
    staff = Staff.query.all()
    if staff:
        return [member.get_json() for member in staff]
    else:
        return []