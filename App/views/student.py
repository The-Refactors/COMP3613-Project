from flask import Blueprint, jsonify, request
from flask_login import login_required
from App.controllers import (
    create_student,
    get_all_students_json,
    get_student_by_id,
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student/all', methods=['GET'])
@login_required
def browse_students():
    students = get_all_students_json()
    return jsonify(students)

@student_views.route('/student/<int:student_id>', methods=['GET'])
@login_required
def view_student(student_id):
    student = get_student_by_id(student_id)
    if student:
        return jsonify(student.get_json())
    return jsonify({'error': 'Student not found'}), 404

@student_views.route('/student', methods=['POST'])
def create_student_action():
    data = request.json
    student = create_student(data['student_id'], data['system_id'])
    if student:
        return jsonify({'message': f"Student {data['student_id']} created"})
    return jsonify({'error': 'Failed to create student'}), 400
