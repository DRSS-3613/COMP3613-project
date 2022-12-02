from App.database import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    url = db.Column(db.String(120), nullable=False)
    rankings = db.relationship("Ranking", backref="image", lazy=True)

    def __init__(self, user_id, url):
        self.user_id = user_id
        self.url = url

    # Accessors
    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_all_rankings(self):
        return self.rankings

    # moved this logic to image controller
    def get_average_rank(self):
        rankings = self.rankings
        if len(rankings) == 0:
            return 0
        total = 0
        for ranking in rankings:
            total += ranking.rank
        return total / len(rankings)

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "rank": self.get_average_rank(),
            "num_rankings": len(self.rankings),
            "url": self.url,
        }
