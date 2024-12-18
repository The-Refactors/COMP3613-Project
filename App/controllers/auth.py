from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from flask_login import LoginManager

from App.models import User


def jwt_authenticate(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"Found user: {user}")  # Debug log
        if user.check_password(password):
            print(f"Password match for user: {username}")  # Debug log
            return user
        else:
            print(f"Invalid password for user: {username}")  # Debug log
    else:
        print(f"User not found: {username}")  # Debug log
    return None

def signup(username, password, firstname, lastname, email):
    from .staff import create_staff
    
    user = User.query.filter_by(username=username).first()
    if user == None:
        user = create_staff(username, firstname, lastname, password, email)
        return user
    else:
        print(f"Username already taken")  # Debug log
    return None


def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt