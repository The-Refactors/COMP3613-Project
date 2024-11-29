from App.models import Review
from App.database import db

#def create_review(staff, student, isPositive, points, details):
def create_review(staff, student, points, details):

  new_review = Review(staff=staff,
                     student=student,
                     #isPositive=isPositive,
                     points=points,
                     details=details,
                     #studentSeen=False
                    )
  db.session.add(new_review)
  try:
    db.session.commit()
    return new_review
  except Exception as e:
    print("[review.create_review] Error occurred while creating new review: ",
          str(e))
    db.session.rollback()
    return None


def delete_review(review_id):
  review = Review.query.filter_by(id=review_id).first()
  if review:
    db.session.delete(review)
    try:
      db.session.commit()
      return True
    except Exception as e:
      print("[review.delete_review] Error occurred while deleting review: ",
            str(e))
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


def get_total_review_points(student_id):
  reviews = get_student_reviews(student_id)
  sum = 0
  if reviews:
    for review in reviews:
      sum += review.points
  return sum

def get_average_review_points(student_id):
    reviews = get_student_reviews(student_id)
    average = 0
    if reviews:
        average = get_total_review_points(student_id) / len(reviews)
    return average


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
  return reviews

def get_student_reviews(student_id):
  return Review.query.filter_by(student_id=student_id).all()

def get_student_reviews_json(student_id):
  reviews = Review.query.filter_by(student_id=student_id).all()
  if reviews:
    reviews_json = [review.get_json() for review in reviews]
    return reviews_json 
  return None
  
