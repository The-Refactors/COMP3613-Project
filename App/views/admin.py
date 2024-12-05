from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required
from App.controllers import (
    create_admin,
    get_all_admins,
    get_all_admins_json,
)

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

@admin_views.route('/admins', methods=['GET'])
def get_admin_page():
    admins = get_all_admins()
    return render_template('admins.html', admins=admins)

@admin_views.route('/api/admins', methods=['GET'])
def get_admins_action():
    admins = get_all_admins_json()
    return jsonify(admins)

@admin_views.route('/api/admins', methods=['POST'])
def create_admin_endpoint():
    data = request.json
    create_admin(data['username'], data['firstname'], data['lastname'], data['email'], data['password'])
    return jsonify({'message': f"Admin {data['username']} created"})

@admin_views.route('/admins', methods=['POST'])
def create_admin_action():
    data = request.form
    flash(f"Admin {data['username']} created!")
    create_admin(data['username'], data['firstname'], data['lastname'], data['email'], data['password'])
    return redirect(url_for('admin_views.get_admin_page'))
