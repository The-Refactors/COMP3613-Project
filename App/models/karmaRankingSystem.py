from App.database import db
from .karmaObserver import KarmaObserver


class KarmaRankingSystem(db.Model):

    __tablename__ = 'karmaRankingSystem'
    id = db.Column(db.Integer, primary_key=True)
    observers = db.relationship('KarmaObserver', backref='karma_observers', lazy='joined')

    __mapper_args__ = {
        "polymorphic_identity": "karma_ranking_system"
    }

    def notify_of_rank(self, observer_id, rank):

        observer = KarmaObserver.query.filter_by(id=observer_id).first()
        observer.set_karma_rank(rank)

    # notifys all karma observers of their new rank
    def update_ranking(self):

        # query of all karma observers in descending order by their karma value
        sorted_query = KarmaObserver.query.order_by(KarmaObserver.karma.desc()).all()

        rank = 0
        last_karma = 0

        # loop for assigning new karma ranks to all observers
        for observer in sorted_query:
            if not (observer.karma == last_karma):
                rank += 1
            self.notify_of_rank(observer.id, rank)
            last_karma = observer.karma

        db.session.commit()
