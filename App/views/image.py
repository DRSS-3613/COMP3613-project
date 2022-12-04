from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity


from App.controllers import (
    get_user,
    create_image,
    get_image,
    get_images_by_user,
    get_images_by_user_json,
    get_image_rankings,
    get_average_image_rank,
    delete_image,
)

image_views = Blueprint("image_views", __name__, template_folder="../templates")


# Post image route
@image_views.route("/api/image", methods=["POST"])
@jwt_required()
def post_image_action():
    data = request.json
    image = create_image(current_identity.id, data["url"])
    if image:
        return jsonify(image.to_json()), 201
    return jsonify({"message": "Unable to create image"}), 400


# Get image route
@image_views.route("/api/image/<int:id>", methods=["GET"])
@jwt_required()
def get_image_action(id):
    image = get_image(id)
    if image:
        return jsonify(image.to_json()), 200
    return jsonify({"message": "Image not found"}), 404


# Get Images by User route
@image_views.route("/api/image/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_images_by_user_action(user_id):
    user = get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    images = get_images_by_user(user_id)
    if images:
        return jsonify(get_images_by_user_json(user_id)), 200
    return jsonify({"message": "No images found"}), 404


# Get Average Image Rank route
@image_views.route("/api/image/<int:image_id>/rank", methods=["GET"])
@jwt_required()
def get_average_image_rank_action(image_id):
    image = get_image(image_id)
    if image:
        return jsonify({"average_rank": get_average_image_rank(image_id)}), 200
    return jsonify({"message": "Image not found"}), 404


# Get Image Rankings route
@image_views.route("/api/image/<int:image_id>/rankings", methods=["GET"])
@jwt_required()
def get_image_rankings_action(image_id):
    image = get_image(image_id)
    if image:
        return jsonify(get_image_rankings(image_id)), 200
    return jsonify({"message": "Image not found"}), 404


# Delete Image route
@image_views.route("/api/image/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_image_action(id):
    status = delete_image(id)
    if status:
        return jsonify({"message": "Image deleted"}), 200
    return jsonify({"message": "Image not found"}), 404
