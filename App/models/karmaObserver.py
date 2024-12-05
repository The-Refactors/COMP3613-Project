from App.database import db


class KarmaObserver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('karmaRankingSystem.id'))
    karma = db.Column(db.Numeric(precision=6, scale=4), nullable=False, default=0.0)
    karma_rank = db.Column(db.Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "karma_observer"
    }

    # Subscribes to observable KarmaRankingSystem subject
    def observe_system(self, system_id):
        self.system_id = system_id

    def set_karma(self, karma):
        self.karma = karma
        db.session.add(self)
        db.session.commit()
    
    def get_karma(self):
        return self.karma

    def set_karma_rank(self, karma_rank):
        self.karma_rank = karma_rank
    
    def get_karma_rank(self):
        return self.karma_rank
