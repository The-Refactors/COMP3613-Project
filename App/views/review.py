from flask import Blueprint, jsonify, request
from flask_login import login_required
from App.controllers import (
    create_review,
    get_all_reviews_json,
    get_review,
)

review_views = Blueprint('review_views', __name__, template_folder='../templates')

@review_views.route('/review/all', methods=['GET'])
@login_required
def browse_reviews():
    reviews = get_all_reviews_json()
    return jsonify(reviews)

@review_views.route('/review/<int:review_id>', methods=['GET'])
@login_required
def view_review(review_id):
    review = get_review(review_id)
    if review:
        return jsonify(review.to_json())
    return jsonify({'error': 'Review not found'}), 404
