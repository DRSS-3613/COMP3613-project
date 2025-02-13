from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    images = db.relationship(
        "Image", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    rankings = db.relationship(
        "Ranking", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.avatar = "https://gravatar.com/avatar/0020f74200278c9a66fc97e1ffb3e1bf?s=400&d=robohash&r=x"

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_avatar(self):
        return self.avatar

    def set_avatar(self, avatar):
        self.avatar = avatar

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "avatar": self.avatar,
            "images": [image.to_json() for image in self.images],
            "rankings": [ranking.to_json() for ranking in self.rankings],
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
