from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required
from flask_login import login_required

from App.controllers import (
    create_karma_system,
    add_observer_to_system,
    update_karma,
    update_karma_ranking
)

karma_views = Blueprint('karma_views', __name__, template_folder='../templates')

# Create a new Karma Ranking System
@karma_views.route('/karma-system/create', methods=['POST'])
@login_required
def create_karma_system_view():
    karma_system = create_karma_system()
    if karma_system:
        return jsonify({"message": "Karma system created successfully", "id": karma_system.id}), 201
    return jsonify({"error": "Failed to create karma system"}), 500

# Add an observer to a Karma Ranking System
@karma_views.route('/karma-system/<int:system_id>/add-observer/<int:observer_id>', methods=['POST'])
@login_required
def add_observer_to_system_view(system_id, observer_id):
    add_observer_to_system(observer_id, system_id)
    return jsonify({"message": f"Observer {observer_id} added to system {system_id}"}), 200

# Update karma for an observer
@karma_views.route('/karma/update/<int:observer_id>', methods=['POST'])
@login_required
def update_karma_view(observer_id):
    try:
        update_karma(observer_id)
        return jsonify({"message": f"Karma updated for observer {observer_id}"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update karma: {str(e)}"}), 500

# Update karma ranking for a system
@karma_views.route('/karma-system/<int:system_id>/update-ranking', methods=['POST'])
@login_required
def update_karma_ranking_view(system_id):
    try:
        update_karma_ranking(system_id)
        return jsonify({"message": f"Karma rankings updated for system {system_id}"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update karma rankings: {str(e)}"}), 500
