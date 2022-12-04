# import os
import logging
import pytest
import unittest
from werkzeug.security import generate_password_hash

from App.controllers.auth import authenticate
from App.controllers.distributor import (
    create_distributor,
    get_distributor,
    get_distributor_json,
    get_distributor_feeds,
    delete_distributor,
    distribute,
)
from App.controllers.feed import (
    create_feed,
    get_feed,
    get_feeds_by_receiver,
    get_feeds_by_sender,
    get_feed_json,
    view_feed,
    delete_feed,
)
from App.controllers.image import (
    create_image,
    get_image,
    get_images_by_user,
    get_image_json,
    get_average_image_rank,
    get_image_rankings,
    delete_image,
)
from App.controllers.ranking import (
    create_ranking,
    get_ranking,
    get_ranking_json,
    get_rankings_by_ranker,
    get_rankings_by_image,
    update_ranking,
    delete_ranking,
)
from App.controllers.rating import (
    create_rating,
    get_rating,
    get_rating_json,
    get_ratings_by_rater,
    get_ratings_by_rated,
    update_rating,
    delete_rating,
)
from App.controllers.user import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
)
from App.database import create_db
from App.models import User, Image, Rating, Ranking, Feed, Distributor
from wsgi import app

LOGGER = logging.getLogger(__name__)

"""
   Unit Tests
"""


class UserUnitTests(unittest.TestCase):
    def test_create_user(self):
        user = User("bob", "bobpass")
        self.assertEqual(user.username, "bob")

    def test_to_json(self):
        user = User("bob1", "bobpass")
        self.assertDictEqual(
            user.to_json(), {"id": None, "username": "bob1", "images": []}
        )

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method="sha256")
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob3", password)
        assert user.check_password(password)


class ImageUnitTests(unittest.TestCase):
    def test_new_image(self):
        user = User("rob", "robpass")
        image = Image(user.id, "https://www.picsum.com/200/300")
        assert image.user_id == user.id

    def test_to_json(self):
        user = User("rob1", "robpass")
        image = Image(user.id, "https://www.picsum.com/200/300")
        self.assertDictEqual(
            image.to_json(),
            {
                "id": image.id,
                "user_id": user.id,
                "rank": 0,
                "num_rankings": 0,
                "url": "https://www.picsum.com/200/300",
            },
        )

    def test_get_average_rank(self):
        image = Image(1, "https://www.picsum.com/200/300")
        assert image.get_average_rank() == 0


class RatingUnitTests(unittest.TestCase):
    def test_new_rating(self):
        rating = Rating(1, 2, 3)
        assert rating.rating == 3

    def test_to_json(self):
        rating = Rating(1, 2, 3)
        self.assertDictEqual(
            rating.to_json(),
            {
                "id": rating.id,
                "rater_id": 1,
                "rated_id": 2,
                "rating": 3,
            },
        )


class RankingUnitTests(unittest.TestCase):
    def test_new_ranking(self):
        ranking = Ranking(1, 2, 3)
        assert ranking.rank == 3

    def test_to_json(self):
        ranking = Ranking(1, 2, 3)
        self.assertDictEqual(
            ranking.to_json(),
            {
                "id": ranking.id,
                "ranker_id": 1,
                "image_id": 2,
                "rank": 3,
            },
        )


class FeedUnitTests(unittest.TestCase):
    def test_new_feed(self):
        feed = Feed(1, 2, 3)
        assert feed.distributor_id == 3

    def test_to_json(self):
        feed = Feed(1, 2, 3)
        self.assertDictEqual(
            feed.to_json(),
            {
                "id": feed.id,
                "sender_id": 1,
                "receiver_id": 2,
                "distributor_id": 3,
                "seen": False,
            },
        )

    def test_set_seen(self):
        feed = Feed(1, 2, 3)
        feed.set_seen()
        assert feed.seen is True


class DistributorUnitTests(unittest.TestCase):
    def test_new_distributor(self):
        distributor = Distributor(5)
        assert distributor.num_profiles == 5

    def test_to_json(self):
        distributor = Distributor(5)
        self.assertDictEqual(
            distributor.to_json(),
            {
                "id": distributor.id,
                "num_profiles": 5,
                "timestamp": distributor.timestamp,
            },
        )


"""
    Integration Tests
"""


# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and reused for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"})
    create_db(app)
    yield app.test_client()
    # os.unlink(os.getcwd() + "/App/test.db")


def test_authenticate():
    create_user("bob", "bobpass")
    assert authenticate("bob", "bobpass") is not None


# test imported methods from App.controllers.user
class UsersIntegrationTests(unittest.TestCase):
    def test_create_user(self):
        user = create_user("bob1", "bobpass")
        assert user is not None

    def test_create_user_with_existing_username(self):
        create_user("rob", "robpass")
        user2 = create_user("rob", "robpass")
        assert user2 is None

    def test_get_user(self):
        user = create_user("rob1", "robpass")
        user2 = get_user(user.id)
        assert user2.username == "rob1"

    def test_get_user_with_invalid_id(self):
        user = get_user(9080)
        assert user is None

    def test_update_user(self):
        user = create_user("rob2", "robpass")
        user = update_user(user.id, "rob3")
        assert user.username == "rob3"

    def test_update_user_with_invalid_id(self):
        user = update_user(9080, "rob3")
        assert user is None

    def test_delete_user(self):
        user = create_user("rob4", "robpass")
        status = delete_user(user.id)
        assert status is True


# test imported methods from App.controllers.image
class ImagesIntegrationTests(unittest.TestCase):
    def test_create_image(self):
        user = create_user("tom1", "tompass")
        image = create_image(user.id, "https://www.picsum.com/200/300")
        assert image.user_id == user.id

    def test_create_image_with_invalid_user_id(self):
        image = create_image(9080, "https://www.picsum.com/200/300")
        assert image is None

    def test_get_image(self):
        user = create_user("tom2", "tompass")
        image = create_image(user.id, "https://www.picsum.com/200/300")
        image2 = get_image(image.id)
        assert image2.url == image.url

    def test_get_image_with_invalid_id(self):
        image = get_image(9080)
        assert image is None

    def test_get_image_json(self):
        user = create_user("tom3", "tompass")
        image = create_image(user.id, "https://www.picsum.com/200/300")
        self.assertDictEqual(
            get_image_json(image.id),
            {
                "id": image.id,
                "user_id": user.id,
                "rank": 0,
                "num_rankings": 0,
                "url": "https://www.picsum.com/200/300",
            },
        )

    def test_get_images_by_user(self):
        user = create_user("tom4", "tompass")
        create_image(user.id, "https://www.picsum.com/200/300")
        create_image(user.id, "https://www.picsum.com/200/300")
        images = get_images_by_user(user.id)
        assert len(images) == 2

    def test_get_images_by_user_with_invalid_user_id(self):
        images = get_images_by_user(9080)
        assert len(images) == 0

    def test_get_average_image_rank(self):
        user = create_user("tom5", "tompass")
        user2 = create_user("tom6", "tompass")
        image = create_image(user.id, "https://www.picsum.com/200/300")
        create_ranking(user2.id, image.id, 1)
        create_ranking(user2.id, image.id, 3)
        average_rank = get_average_image_rank(image.id)
        assert average_rank == 2

    def test_get_average_image_rank_with_invalid_image_id(self):
        average_rank = get_average_image_rank(9080)
        assert average_rank == 0

    def test_get_image_rankings(self):
        user = create_user("tom7", "tompass")
        user2 = create_user("tom8", "tompass")
        image = create_image(user.id, "https://www.picsum.com/200/300")
        create_ranking(user2.id, image.id, 1)
        create_ranking(user2.id, image.id, 3)
        rankings = get_image_rankings(image.id)
        assert len(rankings) == 2

    def test_delete_image(self):
        user = create_user("tom9", "tompass")
        image = create_image(user.id, "https://www.picsum.com/200/300")
        status = delete_image(image.id)
        assert status is True


# test imported methods from App.controllers.feed
class FeedIntegrationTests(unittest.TestCase):
    def test_create_feed(self):
        feed = create_feed(1, 2, 1)
        assert feed is not None

    def test_create_feed_with_invalid_user_id(self):
        with self.subTest("Invalid sender id"):
            feed = create_feed(9080, 2, 1)
            assert feed is None
        with self.subTest("Invalid receiver id"):
            feed = create_feed(1, 9080, 1)
            assert feed is None

    def test_get_feed(self):
        feed = create_feed(1, 2, 1)
        feed2 = get_feed(feed.id)
        assert feed2 is not None

    def test_get_feed_with_invalid_id(self):
        feed = get_feed(9080)
        assert feed is None

    def test_get_feed_json(self):
        feed = create_feed(1, 2, 1)
        self.assertDictEqual(
            get_feed_json(feed.id),
            {
                "id": feed.id,
                "sender_id": 1,
                "receiver_id": 2,
                "distributor_id": feed.distributor_id,
                "seen": False,
            },
        )

    def test_get_feeds_by_sender(self):
        user = create_user("jane4", "janepass")
        create_feed(user.id, 2, 1)
        create_feed(user.id, 3, 1)
        feeds = get_feeds_by_sender(user.id)
        assert len(feeds) == 2

    def test_get_feeds_by_receiver(self):
        user = create_user("jane5", "janepass")
        create_feed(1, user.id, 1)
        create_feed(2, user.id, 1)
        feeds = get_feeds_by_receiver(user.id)
        assert len(feeds) == 2

    def test_view_feed(self):
        feed = create_feed(1, 2, 1)
        feed = view_feed(feed.id)
        assert feed.seen is True

    def test_view_feed_with_invalid_id(self):
        feed = view_feed(9080)
        assert feed is None

    def test_delete_feed(self):
        feed = create_feed(1, 2, 1)
        status = delete_feed(feed.id)
        assert status is True

    def test_delete_feed_with_invalid_id(self):
        status = delete_feed(9080)
        assert status is False


# test imported methods from App.controllers.rating
class RatingsIntegrationTests(unittest.TestCase):
    def test_create_rating(self):
        rating = create_rating(1, 2, 5)
        assert rating.rated_id == 2

    def test_create_rating_with_invalid_user_id(self):
        with self.subTest("Invalid rater id"):
            rating = create_rating(9080, 2, 5)
            assert rating is None
        with self.subTest("Invalid rated id"):
            rating = create_rating(1, 9080, 5)
            assert rating is None

    def test_get_rating(self):
        rating = create_rating(1, 2, 5)
        rating2 = get_rating(rating.id)
        assert rating2.rated_id == rating.rated_id

    def test_get_rating_with_invalid_id(self):
        rating = get_rating(9080)
        assert rating is None

    def test_get_rating_json(self):
        rating = create_rating(1, 2, 5)
        self.assertDictEqual(
            get_rating_json(rating.id),
            {"id": rating.id, "rater_id": 1, "rated_id": 2, "rating": 5},
        )

    def test_get_ratings_by_rater(self):
        user = create_user("jane2", "janepass")
        create_rating(user.id, 2, 5)
        create_rating(user.id, 3, 3)
        ratings = get_ratings_by_rater(user.id)
        assert len(ratings) == 2

    def test_get_ratings_by_rated(self):
        user = create_user("jane3", "janepass")
        create_rating(1, user.id, 5)
        create_rating(2, user.id, 3)
        ratings = get_ratings_by_rated(user.id)
        assert len(ratings) == 2

    def test_update_rating(self):
        rating = create_rating(1, 2, 5)
        rating = update_rating(rating.id, 3)
        assert rating.rating == 3

    def test_update_rating_with_invalid_id(self):
        rating = update_rating(9080, 3)
        assert rating is None

    def test_delete_rating(self):
        rating = create_rating(1, 2, 5)
        status = delete_rating(rating.id)
        assert status is True

    def test_delete_rating_with_invalid_id(self):
        status = delete_rating(9080)
        assert status is False


# test imported methods from App.controllers.ranking
class RankingsIntegrationTests(unittest.TestCase):
    def test_create_ranking(self):
        image = create_image(1, "https://www.picsum.com/200/300")
        ranking = create_ranking(2, image.id, 5)
        assert ranking.image_id == image.id

    def test_create_ranking_with_invalid_id(self):
        with self.subTest("Invalid image id"):
            ranking = create_ranking(2, 9080, 5)
            assert ranking is None
        with self.subTest("Invalid user id"):
            ranking = create_ranking(9080, 1, 5)
            assert ranking is None

    def test_get_ranking(self):
        ranking = create_ranking(1, 2, 5)
        ranking2 = get_ranking(ranking.id)
        assert ranking2.image_id == ranking.image_id

    def test_get_ranking_with_invalid_id(self):
        ranking = get_ranking(9080)
        assert ranking is None

    def test_get_ranking_json(self):
        ranking = create_ranking(1, 2, 5)
        self.assertDictEqual(
            get_ranking_json(ranking.id),
            {"id": ranking.id, "ranker_id": 1, "image_id": 2, "rank": 5},
        )

    def test_get_rankings_by_user(self):
        user = create_user("jane1", "janepass")
        create_ranking(user.id, 2, 5)
        create_ranking(user.id, 3, 3)
        rankings = get_rankings_by_ranker(user.id)
        assert len(rankings) == 2

    def test_get_rankings_by_user_with_invalid_user_id(self):
        rankings = get_rankings_by_ranker(9080)
        assert len(rankings) == 0

    def test_get_rankings_by_image(self):
        image = create_image(1, "https://www.picsum.com/200/300")
        create_ranking(2, image.id, 5)
        create_ranking(3, image.id, 3)
        rankings = get_rankings_by_image(image.id)
        assert len(rankings) == 2

    def test_get_rankings_by_image_with_invalid_image_id(self):
        rankings = get_rankings_by_image(9080)
        assert len(rankings) == 0

    def test_update_ranking(self):
        ranking = create_ranking(1, 2, 5)
        ranking = update_ranking(ranking.id, 3)
        assert ranking.rank == 3

    def test_delete_ranking(self):
        ranking = create_ranking(1, 2, 5)
        status = delete_ranking(ranking.id)
        assert status is True

    def test_delete_ranking_with_invalid_id(self):
        status = delete_ranking(9080)
        assert status is False


# test imported methods from App.controllers.distributor
class DistributorsIntegrationTests(unittest.TestCase):
    def test_create_distributor(self):
        distributor = create_distributor()
        assert distributor is not None

    def test_get_distributor(self):
        distributor = create_distributor()
        distributor2 = get_distributor(distributor.id)
        assert distributor2.timestamp == distributor.timestamp

    def test_get_distributor_with_invalid_id(self):
        distributor = get_distributor(9080)
        assert distributor is None

    def test_get_distributor_json(self):
        num_users = len(get_all_users())
        distributor = create_distributor()
        self.assertDictEqual(
            get_distributor_json(distributor.id),
            {
                "id": distributor.id,
                "num_profiles": num_users,
                "timestamp": distributor.timestamp,
            },
        )

    def test_delete_distributor(self):
        distributor = create_distributor()
        status = delete_distributor(distributor.id)
        assert status is True

    def test_delete_distributor_with_invalid_id(self):
        status = delete_distributor(9080)
        assert status is False

    def test_distribute(self):
        distributor = create_distributor()
        num_users = len(get_all_users())
        distribute()
        num_feeds = len(get_distributor_feeds(distributor.id))
        assert num_feeds == num_users
