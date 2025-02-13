from App.models import Image
from App.controllers import get_user
from App.database import db


def create_image(user_id, url):
    user = get_user(user_id)
    if user:
        image = Image(user_id, url)
        db.session.add(image)
        db.session.commit()
        return image
    return None


def get_image(id):
    image = Image.query.get(id)
    return image


def get_image_json(id):
    image = Image.query.get(id)
    if image:
        return image.to_json()
    return []


def get_all_images():
    images = Image.query.all()
    return images


def get_all_images_json():
    images = Image.query.all()
    return [image.to_json() for image in images]


def get_images_by_user(user_id):
    images = Image.query.filter_by(user_id=user_id).all()
    return images


def get_images_by_user_json(user_id):
    images = Image.query.filter_by(user_id=user_id).all()
    return [image.to_json() for image in images]


def get_average_image_rank(image_id):
    image = get_image(image_id)
    if image:
        return image.get_average_rank()
    return 0


def get_image_rankings(image_id):
    image = get_image(image_id)
    if image:
        return image.get_all_rankings()
    return []


def get_image_rankings_json(image_id):
    rankings = get_image_rankings(image_id)
    return [ranking.to_json() for ranking in rankings]


def delete_image(id):
    image = get_image(id)
    if image:
        db.session.delete(image)
        db.session.commit()
        return True
    return False
