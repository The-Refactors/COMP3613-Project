from App.database import db

class KarmaRankingSystem(db.Model):

    __tablename__ = 'karmaRankingSystem'
    id = db.Column(db.Integer, primary_key=True)
    observers = db.relationship('KarmaObserver', backref='karma_observers', lazy='joined')

    __mapper_args__ = {
        "polymorphic_identity": "karma_ranking_system"
    }

    def notify_of_rank(self, observer_id, rank):
        from .karmaObserver import KarmaObserver
        
        observer = KarmaObserver.query.filter_by(id=observer_id).first()
        observer.set_karma_rank(rank)

    # notifys all karma observers of their new rank
    def update_ranking(self):
        from .karmaObserver import KarmaObserver

        # query of all karma observers in descending order by their karma value
        sorted_query = KarmaObserver.query.order_by(KarmaObserver.karma.desc()).all()

        rank = 1

        # loop for assigning new karma ranks to all observers
        for observer in sorted_query:
            self.notify_of_rank(observer.id, rank)
            print(f'#{rank} - {observer.id}: {observer.karma}')
            rank += 1

        db.session.commit()
        