from App.database import db


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    sender = db.relationship("User", foreign_keys=[sender_id])
    receiver = db.relationship("User", foreign_keys=[receiver_id])
    distributor_id = db.Column(
        db.Integer, db.ForeignKey("distributor.id"), nullable=False
    )
    seen = db.Column(db.Boolean, default=False)

    def __init__(self, sender_id, receiver_id, distributor_id):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.distributor_id = distributor_id
        self.seen = False

    def get_id(self):
        return self.id

    def get_distributor_id(self):
        return self.distributor_id

    def is_seen(self):
        return self.seen

    def set_seen(self):
        self.seen = True

    def to_json(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "distributor_id": self.distributor_id,
            "seen": self.seen,
        }
