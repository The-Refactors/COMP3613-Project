from App.database import db
from App.models import KarmaRankingSystem, KarmaObserver, Student


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
    new_karma = 0.5 # Neutral karma
    if not reviews:
        return new_karma
    review_points = [review.points for review in reviews]

    # Wilscon Score
    z_sqr = 1.96 * 1.96
    num_rev = len(review_points)
    p_hat = ((sum(review_points) / (num_rev * 3)) + 1) / 2
    new_karma = (p_hat + z_sqr/(2 * num_rev)) / (1 + (z_sqr/num_rev))

    print(f'New Karma: {new_karma}')

    return new_karma

def update_karma(observer_id):
    observer = Student.query.filter_by(id=observer_id).first()

    print(f'Old Karma: {observer.karma}')
    print(f'Karma Rank: {observer.karma_rank}')

    observer.set_karma(calculate_karma(observer.reviews))

    print("Updated karma")

def update_karma_rankings(system_id):
    print("Updates karma rankings")
    

    