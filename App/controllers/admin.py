from App.models import Admin, Student, Staff
from App.database import db 

from .staff import (create_staff)
from .student import(create_student)
from .review import(create_review)


def create_admin(username, firstname, lastname, email, password):
  newAdmin = Admin(username, firstname, lastname, email, password)
  db.session.add(newAdmin)
  try:
    db.session.commit()
    return True
    # can return if we need
    # return newStaff
  except Exception as e:
    print("[admin.create_admin] Error occurred while creating new admin: ", str(e))
    db.session.rollback()
    return False
    
def add_teacher(username,firstname, lastname, email, password):
    if create_staff(username,firstname, lastname, email, password):
        return True
    else:
        print("[admin.add_teacher] Error occurred while creating new staff: ")
        return False

def add_student(username, firstname, lastname, email, password, faculty, admittedTerm, yearofStudy, degree, gpa):
    if create_student(studentID):
        return True
    else:
        print("[admin.add_student] Error occurred while creating new student: ")
        return False

def admin_update_name(userID, firstname, lastname):
    if update_name(userID, firstname, lastname):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the name of user: "+userID)
        return False

def admin_update_username(userID, username):
    if update_username(userID, username):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the username of user: "+userID)
        return False

def admin_update_email(userID, email):
    if update_email(userID, email):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the email of user: "+userID)
        return False

def admin_update_password(userID, password):
    if update_password(userID, password):
        return True
    else:
        print("[admin_update_name] Error occurred while updating the password of user: "+userID)
        return False

