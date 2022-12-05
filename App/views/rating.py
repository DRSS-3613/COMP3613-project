from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required


from App.controllers import (
    get_user,
    create_rating,
    get_rating_json,
    get_ratings_by_rater,
    get_ratings_by_rater_json,
    get_ratings_by_rated,
    get_ratings_by_rated_json,
    get_average_rating_by_rated,
    get_rating,
    update_rating,
    delete_rating,
)

rating_views = Blueprint("rating_views", __name__, template_folder="../templates")


# Create Rating route
@rating_views.route("/api/ratings", methods=["POST"])
@jwt_required()
def create_rating_action():
    data = request.json
    if get_user(data["rater_id"]) and get_user(data["rated_id"]):
        rating = create_rating(data["rater_id"], data["rated_id"], data["rating"])
        return jsonify(get_rating_json(rating.get_id())), 201
    elif not get_user(data["rater_id"]):
        return jsonify({"message": "Rater does not exist"}), 404
    elif not get_user(data["rated_id"]):
        return jsonify({"message": "Rated does not exist"}), 404
    else:
        return jsonify({"message": "Something went wrong"}), 500


# Get Rating
@rating_views.route("/api/ratings/<int:id>", methods=["GET"])
@jwt_required()
def get_rating_action(id):
    rating = get_rating(id)
    if rating:
        return jsonify(get_rating_json(id)), 200
    else:
        return jsonify({"message": "Rating does not exist"}), 404


# Get Ratings by Rater route
@rating_views.route("/api/ratings/rater/<int:rater_id>", methods=["GET"])
@jwt_required()
def get_ratings_by_rater_action(rater_id):
    ratings = get_ratings_by_rater(rater_id)
    if ratings:
        return jsonify(get_ratings_by_rater_json(rater_id)), 200
    else:
        return jsonify({"message": "Rater does not exist"}), 404


# Get Ratings by Rated route
@rating_views.route("/api/ratings/rated/<int:rated_id>", methods=["GET"])
@jwt_required()
def get_ratings_by_rated_action(rated_id):
    ratings = get_ratings_by_rated(rated_id)
    if ratings:
        return jsonify(get_ratings_by_rated(rated_id)), 200
    else:
        return jsonify({"message": "Rated does not exist"}), 404


# Get Average Rating by Rated route
@rating_views.route("/api/ratings/rated/<int:rated_id>/average", methods=["GET"])
@jwt_required()
def get_average_rating_by_rated_action(rated_id):
    average = get_average_rating_by_rated(rated_id)
    if average:
        return jsonify({"average": average}), 200
    else:
        return jsonify({"message": "Rated does not exist"}), 404


# Update Rating route
@rating_views.route("/api/ratings/<int:id>", methods=["PUT"])
@jwt_required()
def update_rating_action(id):
    data = request.json
    status = update_rating(id, data["rating"])
    if status:
        return jsonify(get_rating_json(id)), 200
    else:
        return jsonify({"message": "Rating does not exist"}), 404


# Delete Rating route
@rating_views.route("/api/ratings/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_rating_action(id):
    status = delete_rating(id)
    if status:
        return jsonify({"message": "Rating deleted"}), 200
    else:
        return jsonify({"message": "Rating does not exist"}), 404
