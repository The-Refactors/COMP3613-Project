from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required


from.index import index_views

from App.models import Student, Staff, User, Review

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_staff_by_id,
    get_student_by_student_id,
    create_student,
    create_review
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/home', methods=['GET'])
def home_page():
    users = User.query.all()
    students = Student.query.all()
    rankings = Student.query.order_by(Student.karma.desc()).all()
    staff = Staff.query.all()
    reviews = Review.query.order_by(Review.id.desc()).all()
    my_reviews = Review.query.order_by(Review.id.desc()).filter_by(staff_id=current_user.id)

    def jinja_get_student(student_id):
        student = Student.query.filter_by(id=student_id).first()
        return student

    def jinja_get_staff(staff_id):
        staff = Staff.query.filter_by(id=staff_id).first()
        return staff

    return render_template(f'{current_user.user_type}_home.html', current_user=current_user, users=users, rankings=rankings, students=students, staff=staff, reviews=reviews, my_reviews=my_reviews, jinja_get_student=jinja_get_student, jinja_get_staff=jinja_get_staff)

@user_views.route('/write', methods=['GET'])
def write_review_page():
    reviews = Review.query.all()
    students = Student.query.all()
    staff = Staff.query.all()
    users = User.query.all()
    return render_template('write_review.html', current_user=current_user, reviews=reviews, students=students, staff=staff, users=users)

@user_views.route('/write/post', methods=['POST'])
def write_review_action():
    data = request.form
    print(current_user.id)
    print(data['student_id'])
    print(data['points'])
    print(data['details'])

    staff = get_staff_by_id(current_user.id)
    student = get_student_by_student_id(data['student_id'])

    if student == None:
        student = create_student(data['student_id'], 1)

    review = create_review(current_user, student, data['points'], data['details'])
    message = "Review could not be created. Invalid data"

    if review:
        print("Review successfully created")
        return redirect("/home")

    return render_template('login.html', message=message)



@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')