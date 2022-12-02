from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "images": [image.to_json() for image in self.images],
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
