from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    get_user,
    get_user_by_username,
    update_user,
    delete_user,
    login_user,
    logout_user,
    # get_level,
    authenticate,
)

user_views = Blueprint("user_views", __name__, template_folder="../templates")


@user_views.route("/users", methods=["GET"])
def get_user_page():
    users = get_all_users()
    return render_template("users.html", users=users)


@user_views.route("/static/users")
def static_user_page():
    return send_from_directory("static", "static-user.html")


@user_views.route("/api/users", methods=["POST"])
def create_user_action():
    data = request.json
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "Username Already Taken"})
    user = create_user(data["username"], data["password"])
    return jsonify({"message": "User Created"})


@user_views.route("/api/users", methods=["GET"])
def get_all_users_action():
    users = get_all_users_json()
    return jsonify(users)


@user_views.route("/api/users/byid", methods=["GET"])
def get_user_action():
    data = request.json
    user = get_user(data["id"])
    if user:
        return user.to_json()
    return jsonify({"message": "User Not Found"})


# @user_views.route('/api/users/byid', methods=['GET'])
# def get_user_action():
#     id = request.args.get('id')
#     user = get_user(id)
#     if user:
#         return user.to_json()
#     return jsonify({"message":"User Not Found"})


@user_views.route("/api/users", methods=["PUT"])
def update_user_action():
    data = request.json
    user = update_user(data["id"], data["username"])
    if user:
        return jsonify({"message": "User Updated"})
    return jsonify({"message": "User Not Found"})


@user_views.route("/api/users", methods=["DELETE"])
def delete_user_action():
    data = request.json
    if get_user(data["id"]):
        delete_user(data["id"])
        return jsonify({"message": "User Deleted"})
    return jsonify({"message": "User Not Found"})


@user_views.route("/api/users/identify", methods=["GET"])
@jwt_required()
def identify_user_action():
    return jsonify(
        {
            "message": f"username: {current_identity.username}, id : {current_identity.id}"
        }
    )


@user_views.route("/auth", methods=["POST"])
def login_user_action():
    data = request.get_json()
    user = authenticate(data["username"], data["password"])
    if user:
        login_user(user, False)
        session["username"] = user.username
        session["user_id"] = user.id
        return jsonify({"message": f"{user.username} logged in"})
    return jsonify({"message": "Username and password do not match"})


@user_views.route("/api/users/level", methods=["GET"])
def get_level_action():
    data = request.json
    user = get_user(data["userId"])
    if user:
        level = get_level(user.id)
        return jsonify({"level": f"{level}"})
    return jsonify({"message": "User Not Found"})
