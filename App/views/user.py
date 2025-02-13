from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity


from App.controllers import (
    create_user,
    get_user_json,
    get_all_users_json,
    get_user,
    get_user_by_username,
    delete_user,
    get_ratings_by_rated_json,
    get_average_rating_by_rated,
    get_images_by_user_json,
    distribute_all,
)

user_views = Blueprint("user_views", __name__, template_folder="../templates")


@user_views.route("/identify", methods=["GET"])
@jwt_required()
def identify():
    return jsonify(
        {
            "id": current_identity.id,
            "username": current_identity.username,
        }
    )


# Sign up route
@user_views.route("/api/users", methods=["POST"])
def signup_action():
    data = request.json
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "Username taken."}), 400
    user = create_user(data["username"], data["password"])
    if user:
        distribute_all()
        return jsonify({"message": f"user {data['username']} created"}), 201
    return jsonify({"message": "User not created"}), 400


# Set User Avatar route
@user_views.route("/api/users/<int:id>/avatar", methods=["PUT"])
@jwt_required()
def set_user_avatar(id):
    data = request.json
    user = get_user(id)
    if user:
        if user.id == current_identity.id:
            set_user_avatar(id, data["avatar"])
            return jsonify({"message": "Avatar updated"}), 200
        return jsonify({"message": "You can only update your own avatar"}), 400
    return jsonify({"message": "User not found"}), 404


# Get all users route
@user_views.route("/api/users", methods=["GET"])
@jwt_required()
def get_users_all_action():
    users = get_all_users_json()
    if users:
        return jsonify(users), 200
    return jsonify({"message": "No users found"}), 404


# Get user by id route
@user_views.route("/api/users/<int:id>", methods=["GET"])
@jwt_required()
def get_user_by_id_action(id):
    user = get_user(id)
    if user:
        return jsonify(get_user_json(id)), 200
    return jsonify({"message": "User not found"}), 404


# Get User Summary
@user_views.route("/api/users/<int:id>/summary", methods=["GET"])
@jwt_required()
def get_user_summary_action(id):
    user = get_user(id)
    if user:
        summary = {
            "id": user.get_id(),
            "username": user.get_username(),
            "avatar": user.get_avatar(),
            "images": get_images_by_user_json(user.get_id()),
            "average_rating": get_average_rating_by_rated(user.get_id()),
            "ratings": get_ratings_by_rated_json(user.get_id()),
        }
        return jsonify(summary), 200
    return jsonify({"message": "User not found"}), 404


# Delete user route
@user_views.route("/api/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user_action(id):
    user = get_user(id)
    if user:
        delete_user(id)
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404
