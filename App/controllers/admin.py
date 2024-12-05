from App.database import db
from App.models import Admin


def create_admin(username, firstname, lastname, password, email):
  new_admin = Admin(username=username, firstname=firstname, lastname=lastname, password=password, email=email)
  db.session.add(new_admin)
  try:
    db.session.commit()
    return new_admin
  except Exception as e:
    print("[admin.create_admin] Error occurred while creating new admin: ", str(e))
    db.session.rollback()
    return False
    
def get_all_admins():
    admins = Admin.query.all()
    if admins:
        return admins
    else:
        return None


def get_all_admins_json():
    admins = Admin.query.all()
    if admins:
        return [admin.get_json() for admin in admins]
    else:
        return []
