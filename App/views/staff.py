from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required
from App.controllers import (
    create_staff,
    get_all_staff_json,
    get_staff_by_id,
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/all', methods=['GET'])
@login_required
def browse_staff():
    staff_members = get_all_staff_json()
    return jsonify(staff_members)

@staff_views.route('/staff/<int:staff_id>', methods=['GET'])
@login_required
def view_staff(staff_id):
    staff = get_staff_by_id(staff_id)
    if staff:
        return jsonify(staff.get_json())
    return jsonify({'error': 'Staff member not found'}), 404

@staff_views.route('/staff', methods=['POST'])
def create_staff_action():
    data = request.form
    flash(f"Staff {data['username']} created!")
    create_staff(data['username'], data['firstname'], data['lastname'], data['email'], data['password'])
    return redirect(url_for('staff_views.browse_staff'))
