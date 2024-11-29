from App.database import db
from App.models import KarmaRankingSystem, KarmaObserver


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
    observer = KarmaObserver.query.filter_by(observer_id)
    observer.system_id = system_id

def calculate_karma(reviews):
    new_karma = 0

    for review in reviews:
        new_karma += review.points

    print(new_karma)

    return new_karma

def update_karma(observer_id):
    observer = KarmaObserver.query.filter_by(id=observer_id).first()

    print(observer.karma)
    print(observer.karma_rank)

    observer.set_karma(calculate_karma(observer.reviews))

    print("Updated karma")

def update_karma_rankings(system_id):
    print("Updates karma rankings")
    

    