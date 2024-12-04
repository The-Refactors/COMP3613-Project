from flask import Blueprint, request, jsonify
from App.controllers.auth import login

login_views = Blueprint('login_views', __name__)

@login_views.route('/login', methods=['POST'])
def login_view():
    data = request.json
    print(f"Received data: {data}")  # Debug log

    # Validate input data
    if not data or 'username' not in data or 'password' not in data:
        print("Missing username or password")  # Debug log
        return jsonify({"error": "Username and password are required"}), 400

    user = login(data['username'], data['password'])
    if not user:
        print(f"Invalid login for username: {data['username']}")  # Debug log
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": user.get_json()
    }), 200
