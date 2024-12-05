from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, make_response
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.database import db
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime
from App.controllers import (
    create_review,
    get_all_reviews_json,
    get_review,
    delete_review
)

from App.models import Staff, Student, User, Review

review_views = Blueprint('review_views', __name__, template_folder='../templates')

@review_views.route('/review/all/', methods=['GET'])
@login_required
def browse_reviews():
    reviews = Review.query.all()
    students = Student.query.all()
    staff = Staff.query.all()
    users = User.query.all()
    selected = None

    def jinja_get_student(student_id):
        student = Student.query.filter_by(id=student_id).first()
        return student

    return render_template('browse_reviews.html', current_user=current_user, reviews=reviews, students=students, staff=staff, users=users, selected=selected, jinja_get_student=jinja_get_student)

@review_views.route('/review/all/<int:selected_id>', methods=['GET'])
@login_required
def browse_reviews_selected(selected_id=1):
    reviews = Review.query.all()
    students = Student.query.all()
    staff = Staff.query.all()
    users = User.query.all()
    selected = Review.query.filter_by(id=selected_id).first()

    def jinja_get_student(student_id):
        student = Student.query.filter_by(id=student_id).first()
        return student

    return render_template('browse_reviews.html', current_user=current_user, reviews=reviews, students=students, staff=staff, users=users, selected=selected, jinja_get_student=jinja_get_student)

@review_views.route('/review/<int:review_id>', methods=['GET'])
@login_required
def view_review(review_id):
    review = get_review(review_id)
    if review:
        return jsonify(review.to_json())
    return jsonify({'error': 'Review not found'}), 404

@review_views.route('/review/delete/<int:review_id>', methods=['GET'])
@login_required
def delete_review_action(review_id):
    delete_review(review_id)
    return redirect("/review/all")