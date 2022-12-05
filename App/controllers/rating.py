from App.models import Rating
from App.controllers import get_user
from App.database import db


def create_rating(rater_id, rated_id, rating):
    rater = get_user(rater_id)
    rated = get_user(rated_id)
    if rater and rated:
        rating = Rating(rater_id, rated_id, rating)
        db.session.add(rating)
        db.session.commit()
        return rating
    return None


def get_rating(id):
    rating = Rating.query.get(id)
    return rating


def get_rating_json(id):
    rating = Rating.query.get(id)
    return rating.to_json()


def get_all_ratings():
    ratings = Rating.query.all()
    return ratings


def get_all_ratings_json():
    ratings = Rating.query.all()
    return [rating.to_json() for rating in ratings]


def get_ratings_by_rater(rater_id):
    ratings = Rating.query.filter_by(rater_id=rater_id).all()
    return ratings


def get_ratings_by_rater_json(rater_id):
    ratings = Rating.query.filter_by(rater_id=rater_id).all()
    return [rating.to_json() for rating in ratings]


def get_ratings_by_rated(rated_id):
    ratings = Rating.query.filter_by(rated_id=rated_id).all()
    return ratings


def get_ratings_by_rated_json(rated_id):
    ratings = Rating.query.filter_by(rated_id=rated_id).all()
    return [rating.to_json() for rating in ratings]


def get_average_rating_by_rated(rated_id):
    ratings = Rating.query.filter_by(rated_id=rated_id).all()
    if ratings:
        total = 0
        for rating in ratings:
            total += rating.get_rating()
        return round(total / len(ratings))
    return None


def update_rating(id, new_rating):
    rating = Rating.query.get(id)
    if rating:
        rating.set_rating(new_rating)
        db.session.commit()
        return rating
    return None


def delete_rating(id):
    rating = Rating.query.get(id)
    if rating:
        db.session.delete(rating)
        db.session.commit()
        return True
    return False
