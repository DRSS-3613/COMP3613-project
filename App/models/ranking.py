from App.database import db


class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ranker_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("image.id"), nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def __init__(self, ranker_id, image_id, rank):
        self.ranked_id = ranker_id
        self.image_id = image_id
        self.rank = rank

    def to_json(self):
        return {
            "id": self.id,
            "ranker_id": self.ranker_id,
            "image_id": self.image_id,
            "rank": self.rank,
        }
