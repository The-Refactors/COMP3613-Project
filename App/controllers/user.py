from App.database import db
from App.models import User


def create_user(username, firstname, lastname, password, email):
    newuser = User(username=username, firstname=firstname ,lastname=lastname, password=password, email=email)
    db.session.add(newuser)
    try:
        db.session.commit()
        return newuser
    except Exception as e:
        print("[user.create_user] Error occurred while creating new user: ", str(e))
        db.session.rollback()
        return None
    

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    else:
        return None

def get_user(id):
    user = User.query.get(id)
    if user:
        return user
    else:
        return None

#def get_user_student(student):
#  user = User.query.get(student.id)
#  if user:
#      return user
#  else:
#      return None

def get_all_users():
    users = User.query.all()
    if users:
        return users
    else:
        return None

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    return [user.get_json() for user in users]

def update_user_username(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_user_username] Error occurred while creating new user: ", str(e))
            db.session.rollback()
            return False
    return False

def update_username(user_id, new_username):
    user = get_user(user_id)
    if user:
        user.username = new_username
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_username] Error occurred while updating user username:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_username] Error occurred while updating user username: User " + user_id + " not found")
        return False

def update_name(user_id, new_firstname, new_last_name):
    user = get_user(user_id)
    if user:
        user.firstname = new_firstname
        user.lastname = new_last_name
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_name] Error occurred while updating user name:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_name] Error occurred while updating user name: User " + user_id + " not found")
        return False

def update_email(user_id, new_email):
    user = get_user(user_id)
    if user:
        user.email = new_email
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_email] Error occurred while updating user email:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_email] Error occurred while updating user email: User " + user_id + " not found")
        return False

def update_password(user_id, new_password):
    user = get_user(user_id)
    if user:
        user.set_password(new_password)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_password] Error occurred while updating user password:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_password] Error occurred while updating user password: User " + user_id + " not found")
        return False

def update_faculty(user_id, new_faculty):
    user = get_user(user_id)
    if user:
        user.faculty = new_faculty
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_faculty] Error occurred while updating user faculty:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_faculty] Error occurred while updating student faculty: User " + user_id + " not found")
        return False