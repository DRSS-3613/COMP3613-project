from App.models import User
from App.database import db
from App.controllers import get_average_rating_by_rated, get_ratings_by_rated


def create_user(username, password):
    user = get_user_by_username(username)
    if not user:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    return None


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user


def get_user(id):
    return User.query.get(id)


def get_user_json(id):
    user = get_user(id)
    if user:
        return user.to_json()
    return None


def get_all_users():
    return User.query.all()


def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.to_json() for user in users]
    return users


def get_user_summary(id):
    user = get_user(id)
    if user:
        return {
            "id": user.id,
            "username": user.username,
            "images": [image.to_json() for image in user.images],
            "average_rating": get_average_rating_by_rated(user.id),
            "ratings": [rating.to_json() for rating in get_ratings_by_rated(user.id)],
        }
    return None


def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        db.session.commit()
        return user
    return None


def delete_user(id):
    user = get_user(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
