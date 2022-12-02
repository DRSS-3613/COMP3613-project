from App.models import Feed
from App.database import db


def create_feed(sender_id, receiver_id, distributor_id):
    feed = Feed(sender_id, receiver_id, distributor_id)
    db.session.add(feed)
    db.session.commit()
    return feed


def get_feed(id):
    feed = Feed.query.get(id)
    return feed


def get_feed_json(id):
    feed = Feed.query.get(id)
    return feed.to_json()


def get_all_feeds():
    feeds = Feed.query.all()
    return feeds


def get_all_feeds_json():
    feeds = Feed.query.all()
    return [feed.to_json() for feed in feeds]


def get_feeds_by_sender(sender_id):
    feeds = Feed.query.filter_by(sender_id=sender_id).all()
    return feeds


def get_feeds_by_sender_json(sender_id):
    feeds = Feed.query.filter_by(sender_id=sender_id).all()
    return [feed.to_json() for feed in feeds]


def get_feeds_by_receiver(receiver_id):
    feeds = Feed.query.filter_by(receiver_id=receiver_id).all()
    return feeds


def get_feeds_by_receiver_json(receiver_id):
    feeds = Feed.query.filter_by(receiver_id=receiver_id).all()
    return [feed.to_json() for feed in feeds]


def view_feed(id):
    feed = Feed.query.get(id)
    if feed:
        feed.set_seen()
        db.session.commit()
        return feed
    return None


def delete_feed(id):
    feed = Feed.query.get(id)
    if feed:
        db.session.delete(feed)
        return db.session.commit()
    return None
