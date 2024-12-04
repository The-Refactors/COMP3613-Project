from App.database import db
from App.models import KarmaRankingSystem, KarmaObserver
from .student import get_karma_ordered_students_by_system_id, get_student_by_id


def create_karma_system():
    new_karma_system = KarmaRankingSystem()
    db.session.add(new_karma_system)
    try:
        db.session.commit()
        return new_karma_system
    except Exception as e:
        print(
            "Error occurred while creating karma system: ",
            str(e))
        db.session.rollback()
        return False


def add_observer_to_system(observer_id, system_id):
    observer = KarmaObserver.query.filter_by(id=observer_id).first()
    observer.system_id = system_id

def calculate_karma(reviews):
    new_karma = 0
    if not reviews:
        return new_karma
    review_points = [review.points for review in reviews]

    # Wilscon Score
    z_sqr = 1.96 * 1.96
    num_rev = len(review_points)
    p_hat = ((sum(review_points) / (num_rev * 3)) + 1) / 2
    new_karma = (p_hat + z_sqr/(2 * num_rev)) / (1 + (z_sqr/num_rev))

    return new_karma

def update_karma(observer_id):
    observer = get_student_by_id(id=observer_id)
    print(f'Old Karma: {float(observer.karma)}')

    observer.set_karma(calculate_karma(observer.reviews))
    print(f'Updated Karma for student {observer.student_id} to {float(observer.karma)}')

def update_karma_ranking(id):
    # gets karma ranking system (subject) which notifies students (observers) of their new karma rank
    system = KarmaRankingSystem.query.filter_by(id=id).first()
    system.update_ranking()

    print("Updated Karma rankings")

def print_karma_ranking(id):
    students = get_karma_ordered_students_by_system_id(system_id=id)
    for student in students:
        print(f'#{student.karma_rank} - {student.student_id}: {float(student.karma)}')

def get_karma_ranking_json(id):
    students = get_karma_ordered_students_by_system_id(system_id=id)
    jsondata = []
    for student in students:
        jsondata.append({
            "rank": student.karma_rank,
            "student_id": student.student_id,
            "karma": float(student.karma)
        })
    return jsondata