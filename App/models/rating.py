from App.database import db


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rater_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rated_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rater = db.relationship("User", foreign_keys=[rater_id])
    rated = db.relationship("User", foreign_keys=[rated_id])
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, rater_id, rated_id, rating):
        self.rater_id = rater_id
        self.rated_id = rated_id
        self.rating = rating

    def get_id(self):
        return self.id

    def get_rating(self):
        return self.rating

    def get_rater_id(self):
        return self.rater_id

    def get_rated_id(self):
        return self.rated_id

    def set_rating(self, new_rating):
        self.rating = new_rating

    def to_json(self):
        return {
            "id": self.id,
            "rater_id": self.rater_id,
            "rated_id": self.rated_id,
            "rating": self.rating,
        }
