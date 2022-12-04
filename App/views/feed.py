from flask import Blueprint, jsonify
from flask_jwt import jwt_required

from App.controllers import (
    get_user,
    get_feed,
    get_feed_json,
    get_feeds_by_sender,
    get_feeds_by_sender_json,
    get_feeds_by_receiver,
    get_feeds_by_receiver_json,
    view_feed,
)

feed_views = Blueprint("feed_views", __name__, template_folder="../templates")


# Get Feed route
@feed_views.route("/api/feed/<int:id>", methods=["GET"])
@jwt_required()
def get_feed_action(id):
    feed = get_feed(id)
    if feed:
        return jsonify(get_feed_json(id)), 200
    return jsonify({"error": "Feed not found."}), 404


# Get Feeds by Sender route
@feed_views.route("/api/feed/sender/<int:sender_id>", methods=["GET"])
@jwt_required()
def get_feeds_by_sender_action(sender_id):
    user = get_user(sender_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    feeds = get_feeds_by_sender(sender_id)
    if feeds:
        return jsonify(get_feeds_by_sender_json(sender_id)), 200
    return jsonify({"error": "Feeds not found."}), 404


# Get Feeds by Receiver route
@feed_views.route("/api/feed/receiver/<int:receiver_id>", methods=["GET"])
@jwt_required()
def get_feeds_by_receiver_action(receiver_id):
    feeds = get_feeds_by_receiver(receiver_id)
    if feeds:
        return jsonify(get_feeds_by_receiver_json(receiver_id)), 200
    return jsonify({"error": "Feeds not found."}), 404


# View Feed route
@feed_views.route("/api/feed/<int:id>/view", methods=["POST"])
@jwt_required()
def view_feed_action(id):
    feed = view_feed(id)
    if feed:
        return jsonify(get_feed_json(id)), 200
    return jsonify({"error": "Feed not found."}), 404
