from App.database import db
from App.models import Review
from.karmaSystem import update_karma


def create_review(staff, student, points, details):
  new_review = Review(staff=staff,
                     student=student,
                     points=points,
                     details=details)
  db.session.add(new_review)

  try:
    db.session.commit()
    return new_review
  except Exception as e:
    print("[review.create_review] Error occurred while creating new review: ",
          str(e))
    db.session.rollback()
    return None

def update_review_staff(review_id, staff):
    review = get_review(review_id)
    if review:
        review.staff_id = staff.id
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[review.update_review_staff] Error occurred while updating review staff:", str(e))
            db.session.rollback()
            return False
    else:
        print("[review.update_review_staff] Error occurred while updating review staff: Review " + review_id + " not found")
        return False

def update_review_student(review_id, student):
    review = get_review(review_id)
    if review:
        old_student_id = review.student_id
        review.student_id = student.id
        update_karma(old_student_id)
        update_karma(review.student_id)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[review.update_review_student] Error occurred while updating review student:", str(e))
            db.session.rollback()
            return False
    else:
        print("[review.update_review_student] Error occurred while updating review student: Review " + review_id + " not found")
        return False

def update_review_points(review_id, points):
    review = get_review(review_id)
    if review:
        review.points = points
        update_karma(review.student_id)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[review.update_review_points] Error occurred while updating review points:", str(e))
            db.session.rollback()
            return False
    else:
        print("[review.update_review_points] Error occurred while updating review points: Review " + review_id + " not found")
        return False

def update_review_details(review_id, details):
    review = get_review(review_id)
    if review:
        review.details = details
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[review.update_review_details] Error occurred while updating review details:", str(e))
            db.session.rollback()
            return False
    else:
        print("[review.update_review_details] Error occurred while updating review details: Review " + review_id + " not found")
        return False


def delete_review(review_id):
  review = Review.query.filter_by(id=review_id).first()
  if review:
    db.session.delete(review)
    update_karma(review.student_id)
    try:
      db.session.commit()
      return True
    except Exception as e:
      print("[review.delete_review] Error occurred while deleting review: ", str(e))
      db.session.rollback()
      return False
  else:
    return False

#
# def calculate_points_upvote(review):
#   review.points *= 1.1  # multiplier can be changed accordingly
#
#   try:
#     db.session.commit()
#     return True
#   except Exception as e:
#     print(
#         "[review.calculate_points_upvote] Error occurred while updating review points:",
#         str(e))
#     db.session.rollback()
#     return False
#
#
# def calculate_points_downvote(review):
#   review.points *= 0.9
#
#   try:
#     db.session.commit()
#     return True
#   except Exception as e:
#     print(
#         "[review.calculate_points_downvote] Error occurred while updating review points:",
#         str(e))
#     db.session.rollback()
#     return False


# def get_total_review_points(student_id):
#   reviews = get_student_reviews(student_id)
#   sum = 0
#   if reviews:
#     for review in reviews:
#       sum += review.points
#   return sum
#
# def get_average_review_points(student_id):
#     reviews = get_student_reviews(student_id)
#     average = 0
#     if reviews:
#         average = get_total_review_points(student_id) / len(reviews)
#     return average


# def get_total_review_points(student_id):
#   reviews = Review.query.filter_by(studentid=student_id).all()
#   if reviews:
#       total_points = 0
#       review_count = 0
#       for review in reviews:
#
#           capped_points = max(min(review.points, 30), -30)
#           total_points += capped_points / 30
#           if capped_points <= 30 or capped_points >= -30:  # Only count reviews after applying the threshold
#               #print(" review.points:", review.points)
#               review_count += 1
#       if review_count == 0:  # Avoid division by zero
#           return 0
#       #print("Total Points:", total_points)
#       #print("Review Count:", review_count)
#
#       return round(100 * total_points / review_count, 2) # multiplying by 100 to normalize to 100 points
#   return 0

def get_review(id):
  review = Review.query.filter_by(id=id).first()
  if review:
    return review
  else:
    return None
  
def get_all_reviews():
  reviews = Review.query.all()
  if not reviews:
      return None
  return reviews

def get_all_reviews_json():
    reviews = Review.query.all()
    if not reviews:
        return []
    return [review.get_json() for review in reviews]

def get_student_reviews(student_id):
  return Review.query.filter_by(student_id=student_id).all()

def get_student_reviews_json(student_id):
  reviews = Review.query.filter_by(student_id=student_id).all()
  if reviews:
    return [review.get_json() for review in reviews]
  return None
  
