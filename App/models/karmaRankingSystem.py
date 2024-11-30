from App.database import db

class KarmaRankingSystem(db.Model):
    __tablename__ = 'karmaRankingSystem'
    id = db.Column(db.Integer, primary_key=True)
    observers = db.relationship('KarmaObserver', backref='karma_observers', lazy='joined')

    __mapper_args__ = {
        "polymorphic_identity": "karma_ranking_system"
    }

    # def update_ranking():
    #     for observer in observers:
    #         print(f'Updated Student ${observer.id}''s ranking')
        