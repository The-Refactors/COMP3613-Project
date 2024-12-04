from flask import Blueprint, request, jsonify
from App.controllers import jwt_authenticate

login_views = Blueprint('login_views', __name__, template_folder='../templates')

@login_views.route('/login', methods=['POST'])
def login():
    data = request.json
    token = jwt_authenticate(data['username'], data['password'])
    if token:
        return jsonify({'access_token': token})
    return jsonify({'error': 'Invalid credentials'}), 401
