from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required


from App.controllers import (
    get_user,
    get_image,
    create_ranking,
    get_ranking,
    get_ranking_json,
    get_rankings_by_ranker,
    get_rankings_by_ranker_json,
    get_rankings_by_image,
    get_rankings_by_image_json,
    update_ranking,
    delete_ranking,
)

ranking_views = Blueprint("ranking_views", __name__, template_folder="../templates")


# Create Ranking route
@ranking_views.route("/api/ranking", methods=["POST"])
@jwt_required()
def create_ranking_action():
    data = request.json
    if get_user(data["ranker_id"]) and get_image(data["image_id"]):
        ranking = create_ranking(data["ranker_id"], data["image_id"], data["rank"])
        return jsonify(ranking.to_json()), 201
    elif not get_user(data["ranker_id"]):
        return jsonify({"message": "Ranker does not exist"}), 404
    elif not get_image(data["image_id"]):
        return jsonify({"message": "Image does not exist"}), 404
    else:
        return jsonify({"message": "Something went wrong"}), 500


# Get Ranking route
@ranking_views.route("/api/ranking/<int:id>", methods=["GET"])
@jwt_required()
def get_ranking_action(id):
    ranking = get_ranking(id)
    if ranking:
        return jsonify(get_ranking_json(id)), 200
    else:
        return jsonify({"message": "Ranking does not exist"}), 404


# Get Rankings by Ranker route
@ranking_views.route("/api/ranking/ranker/<int:ranker_id>", methods=["GET"])
@jwt_required()
def get_rankings_by_ranker_action(ranker_id):
    user = get_user(ranker_id)
    if not user:
        return jsonify({"message": "Ranker does not exist"}), 404
    rankings = get_rankings_by_ranker(ranker_id)
    if rankings:
        return jsonify(get_rankings_by_ranker_json(ranker_id)), 200
    else:
        return jsonify({"message": "Rankings not found"}), 404


# Get Rankings by Image route
@ranking_views.route("/api/ranking/image/<int:image_id>", methods=["GET"])
@jwt_required()
def get_rankings_by_image_action(image_id):
    image = get_image(image_id)
    if not image:
        return jsonify({"message": "Image does not exist"}), 404
    rankings = get_rankings_by_image(image_id)
    if rankings:
        return jsonify(get_rankings_by_image_json(image_id)), 200
    else:
        return jsonify({"message": "Rankings not found"}), 404


# Update Ranking route
@ranking_views.route("/api/ranking/<int:id>", methods=["PUT"])
@jwt_required()
def update_ranking_action(id):
    data = request.json
    status = update_ranking(id, data["rank"])
    if status:
        return jsonify(get_ranking_json(id)), 200
    else:
        return jsonify({"message": "Ranking does not exist"}), 404


# Delete Ranking route
@ranking_views.route("/api/ranking/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_ranking_action(id):
    status = delete_ranking(id)
    if status:
        return jsonify({"message": "Ranking deleted"}), 200
    else:
        return jsonify({"message": "Ranking does not exist"}), 404
