import os
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from datetime import timedelta


from App.database import create_db, get_migrate

from App.controllers import setup_jwt, load_user_from_id

from App.views import (
    index_views,
)  # user_views, image_views, rating_views, ranking_views,

# New views must be imported and added to this list

views = [index_views]  # user_views, image_views, rating_views, ranking_views, ]


def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config["ENV"] = os.environ.get("ENV", "DEVELOPMENT")
    if app.config["ENV"] == "DEVELOPMENT":
        app.config.from_object("App.config")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI"
        )
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["DEBUG"] = os.environ.get("ENV").upper() != "PRODUCTION"
        app.config["ENV"] = os.environ.get("ENV")
        app.config["JWT_EXPIRATION_DELTA"] = timedelta(
            days=int(os.environ.get("JWT_EXPIRATION_DELTA"))
        )
    for key, value in config.items():
        app.config[key] = config[key]


def create_app(config={}):
    app = Flask(__name__, static_url_path="/static")
    CORS(app)
    loadConfig(app, config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["UPLOADED_PHOTOS_DEST"] = "App/uploads"
    photos = UploadSet("photos", TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    create_db(app)
    setup_jwt(app)
    app.app_context().push()
    return app


app = create_app()
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return load_user_from_id(user_id)


migrate = get_migrate(app)
