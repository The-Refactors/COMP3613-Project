import os, tempfile, pytest, logging, unittest, sys
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from App.main import create_app
from App.database import db, create_db
from App.models import Review, Student, Staff
from App.controllers import (
    create_student,
    create_staff,
    create_review,
    get_review,
    get_all_reviews,
    get_student_reviews,
    delete_review
)
'''
   Unit Tests
'''
class ReviewUnitTests(unittest.TestCase):

    def test_new_review(self):
        student = Student("816023233")
        staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass")
        review = Review(student=student, staff=staff, details="Great!", points=2)
        assert review is not None

    def test_review_get_json(self):
        created = datetime.now()
        student = Student("816023233")
        staff = Staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass")
        review = Review(student=student, staff=staff, details="Great!", points=2, date_created=created)
        review_json = review.get_json()
        self.assertDictEqual({
            "id": None,
            "staff_id": None,
            "student_id": None,
            "date_created": created.strftime("%d-%m-%Y %H:%M"),
            "points": 2,
            "details": "Great!"
        }, review_json)



'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class ReviewIntegrationTests(unittest.TestCase):

    def test_create_review(self):
        student = create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass")
        staff = create_student(student_id="816000000", system_id=1)
        review = create_review(staff=staff, student=student, points=2, details="Joe is good.")
        create_review(staff=staff, student=student, points=1, details="Joe could be better.")
        assert review.details == "Joe is good."


    def test_get_review(self):
        review = get_review(1)
        assert review is not None


    def test_get_all_reviews(self):
        reviews = get_all_reviews()
        assert reviews[0].details == "Joe is good." and reviews[1].details == "Joe could be better."

    def get_student_reviews(self):
        reviews = get_student_reviews(816000000)
        assert reviews[0].details == "Joe is good" and reviews[1].details == "Joe could be better."


    # def test_calc_points_upvote(self):
    #     self.test_create_review()
    #     review = get_review(1)
    #     print(review.to_json(student=get_student_by_id(review.studentid), staff=get_staff_by_id(review.createdByStaffID)))
    #     assert review is not None
    #     assert calculate_points_upvote(review) == True

    # def test_calc_points_downvote(self):
    #     self.test_create_review()
    #     review = get_review(1)
    #     print(review.to_json(student=get_student_by_id(review.studentid), staff=get_staff_by_id(review.createdByStaffID)))
    #     assert review is not None
    #     assert calculate_points_downvote(review) == True

    # def test_get_total_points(self):
    #     self.test_create_review()
    #     review = get_review(1)
    #     assert get_total_review_points(review.studentid) != 0

    # def test_delete_review(self):
    #     self.test_create_review()
    #     review = get_review(2)
    #     assert delete_review(review.id) == True
