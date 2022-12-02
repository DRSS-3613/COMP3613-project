from App.database import db
from App.models import Distributor
from App.controllers.feed import (
    get_feeds_by_sender,
    create_feed,
    get_feeds_by_receiver,
)
from datetime import timedelta, datetime


def create_distributor(num_profiles):
    distributor = Distributor(num_profiles)
    db.session.add(distributor)
    db.session.commit()
    return distributor


def get_distributor(id):
    distributor = Distributor.query.get(id)
    return distributor


def get_distributor_json(id):
    distributor = Distributor.query.get(id)
    return distributor.to_json()


def get_all_distributors():
    distributors = Distributor.query.all()
    return distributors


def get_all_distributors_json():
    distributors = Distributor.query.all()
    return [distributor.to_json() for distributor in distributors]


def get_distributor_feeds(id):
    distributor = Distributor.query.get(id)
    if distributor:
        return distributor.feed
    return None


def distribute(dist_id):
    receivers = []
    senders = []
    distributor = Distributor.query.get(dist_id)
    if distributor:
        # loops through all the profiles for each receiver
        for receiver_id in range(1, distributor.num_profiles + 1):
            # list of feeds for the receiver
            r_feeds = get_feeds_by_receiver(receiver_id)
            # gets the number of feeds that the receiver has gotten in the past day
            daily_receiver_counter = len(
                [
                    feed
                    for feed in r_feeds
                    if feed.distributor.timestamp
                    >= (datetime.now() - timedelta(days=1))
                ]
            )
            # if the receiver has gotten less than the number of profiles per day, they can receive more
            if daily_receiver_counter < distributor.num_profiles:
                # loops through all the profiles for each sender
                for sender_id in range(1, distributor.num_profiles + 1):
                    # gets the number of feeds that the sender has sent in the past day
                    daily_sender_counter = len(
                        [
                            feed
                            for feed in get_feeds_by_sender(sender_id)
                            if feed.distributor.timestamp
                            >= (datetime.now() - timedelta(days=1))
                        ]
                    )
                    # if the sender has sent less than the number of profiles per day, they can send more
                    if daily_sender_counter < distributor.num_profiles:
                        # checks to ensure the receiver hasn't already received a feed from the sender
                        already_received = any(
                            feed.sender_id == sender_id for feed in r_feeds
                        )
                        # if the receiver hasn't already received a feed from the sender and neither has crossed their
                        # limit, create a feed
                        if (
                            (receiver_id != sender_id)
                            and not already_received
                            and (sender_id not in senders)
                        ):
                            create_feed(sender_id, receiver_id, dist_id)
                            senders.append(sender_id)
                            receivers.append(receiver_id)
                            break

        # if the number of receivers is less than the number of profiles, there are no more unique feeds to send
        # therefore repeats must be sent
        if len(receivers) < distributor.num_profiles:
            # loops through all the profiles for each receiver
            for receiver_id in range(1, distributor.num_profiles + 1):
                # if the receiver hasn't received a feed for this distribution, they can receive one
                if receiver_id not in receivers:
                    # gets the number of feeds that the receiver has gotten in the past day
                    daily_receiver_counter = len(
                        [
                            feed
                            for feed in get_feeds_by_receiver(receiver_id)
                            if feed.distributor.timestamp
                            >= (datetime.now() - timedelta(days=1))
                        ]
                    )
                    # if the receiver has gotten less than the number of profiles per day, they can receive more
                    if daily_receiver_counter < distributor.num_profiles:
                        # loops through all the profiles for each sender
                        for sender_id in range(1, distributor.num_profiles + 1):
                            # gets the number of feeds that the sender has sent in the past day
                            daily_sender_counter = len(
                                [
                                    feed
                                    for feed in get_feeds_by_sender(sender_id)
                                    if feed.distributor.timestamp
                                    >= (datetime.now() - timedelta(days=1))
                                ]
                            )
                            # if the sender has sent less than the number of profiles per day, they can send more and
                            # the sender and receiver aren't the same profile and the sender hasn't already sent a feed
                            # to the receiver for this distribution, create a feed
                            if (
                                daily_sender_counter < distributor.num_profiles
                                and sender_id != receiver_id
                                and sender_id not in senders
                            ):
                                create_feed(sender_id, receiver_id, dist_id)
                                senders.append(sender_id)
                                receivers.append(receiver_id)
                                break
        # if after both loops, the number of receivers is still less than the number of profiles, there are no more
        # profiles below the limit and therefore no more feeds can be generated
        if len(senders) < distributor.num_profiles:
            return False
        return True
