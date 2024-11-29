from App.database import db


class KarmaObserver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('karmaRankingSystem.id'))
    karma = db.Column(db.Float, nullable=True)
    karma_rank = db.Column(db.Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "karma_observer"
    }

    def set_karma(self, karma):
        print(f'Setting karma to {karma}')
        self.karma = karma
    
    def get_karma(self):
        return self.karma

    def set_karma_rank(self, karma_rank):
        self.karma_rank = karma_rank
    
    def get_karma_rank(self):
        return self.karma_rank