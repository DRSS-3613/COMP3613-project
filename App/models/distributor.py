from App.database import db
from datetime import datetime


class Distributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_profiles = db.Column(db.Integer, nullable=False)
    feed = db.relationship(
        "Feed", backref="distributor", lazy=True, cascade="all, delete-orphan"
    )
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, num_profiles):
        self.num_profiles = num_profiles

    # Accessors
    def get_id(self):
        return self.id

    def get_num_profiles(self):
        return self.num_profiles

    def get_timestamp(self):
        return self.timestamp

    def get_receivers(self):
        receivers = []
        for feed in self.feed:
            receivers.append(feed.receiver_id)
        return receivers

    def get_senders(self):
        senders = []
        for feed in self.feed:
            senders.append(feed.sender_id)
        return senders

    def to_json(self):
        return {
            "id": self.id,
            "num_profiles": self.num_profiles,
            "timestamp": self.timestamp,
        }
