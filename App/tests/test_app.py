import os, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify
from datetime import date, datetime

from App.database import create_db
from App.models import User, Image, Rating, Ranking, Feed, Distributor

from App.controllers.auth import authenticate
from App.controllers.user import (create_user, get_user, update_user, delete_user)
from App.controllers.image import (create_image, get_image, get_images_by_user, get_image_json, get_average_image_rank, get_image_rankings, delete_image)
from App.controllers.feed import (create_feed)
from App.controllers.rating import (create_rating)
from App.controllers.ranking import (create_ranking)
from App.controllers.distributor import (create_distributor)



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
        user_json = user.to_json()
        self.assertDictEqual(
            user_json, {"id": None, "username": "bob1", "images": []}
        )

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method="sha256")
        user = User("bob2", password)
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
        self.assertDictEqual(image.to_json(), {"id": image.id, "user_id": user.id, "rank": 0, "num_rankings": 0,
                                               "url": "https://www.picsum.com/200/300"})

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
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"})
    create_db(app)
    yield app.test_client()
    # os.unlink(os.getcwd() + "/App/test.db")

#     def test_authenticate():
#         user = create_user("bob", "bobpass")
#         assert authenticate("bob", "bobpass") is not None

class UsersIntegrationTests(unittest.TestCase):
    def test_create_user(self):
        user = create_user("bob", "bobpass")
        assert user.username == "bob"

    def test_create_user_with_existing_username(self):
        user1 = create_user("rob", "robpass")
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
        self.assertDictEqual(get_image_json(image.id), {"id": image.id, "user_id": user.id, "rank": 0, "num_rankings": 0, "url": "https://www.picsum.com/200/300"})

    def test_get_images_by_user(self):
        user = create_user("tom4", "tompass")
        image1 = create_image(user.id, "https://www.picsum.com/200/300")
        image2 = create_image(user.id, "https://www.picsum.com/200/300")
        images = get_images_by_user(user.id)
        assert len(images) == 2

    def test_get_images_by_user_with_invalid_user_id(self):
        images = get_images_by_user(9080)
        assert len(images) == 0

    def test_get_average_image_rank(self):
        user = create_user("tom5", "tompass")
        user2 = create_user("tom6", "tompass")
        image = create_image(user.id, "https://www.picsum.com/200/300")
        ranking1 = create_ranking(user2.id, image.id, 1)
        ranking2 = create_ranking(user2.id, image.id, 3)
        average_rank = get_average_image_rank(image.id)
        assert average_rank == 2

    def test_get_average_image_rank_with_invalid_image_id(self):
        average_rank = get_average_image_rank(9080)
        assert average_rank == 0

    def test_get_image_rankings(self):
        user = create_user("tom7", "tompass")
        user2 = create_user("tom8", "tompass")
        image = create_image(user.id, "https://www.picsum.com/200/300")
        ranking1 = create_ranking(user2.id, image.id, 1)
        ranking2 = create_ranking(user2.id, image.id, 3)
        rankings = get_image_rankings(image.id)
        assert len(rankings) == 2

    def test_delete_image(self):
        user = create_user("tom9", "tompass")
        image = create_image(user.id, "https://www.picsum.com/200/300")
        status = delete_image(image.id)
        assert status is True


#
#
# class RatingIntegrationTests(unittest.TestCase):
#     def test_create_rating(self):
#         rating = create_rating(1, 2, 3)
#         assert rating.id == 1
#
#     def test_get_rating(self):
#         rating = get_rating(1)
#         assert rating.creatorId == 1
#
#     def test_get_all_ratings(self):
#         rating = create_rating(2, 1, 4)
#         ratingList = []
#         ratingList.append(get_rating(1))
#         ratingList.append(get_rating(2))
#         self.assertListEqual(get_all_ratings(), ratingList)
#
#     def test_get_all_ratings_json(self):
#         ratings_json = get_all_ratings_json()
#         self.assertListEqual(
#             [
#                 {
#                     "id": 1,
#                     "creatorId": 1,
#                     "targetId": 2,
#                     "score": 3,
#                     "timeStamp": date.today(),
#                 },
#                 {
#                     "id": 2,
#                     "creatorId": 2,
#                     "targetId": 1,
#                     "score": 4,
#                     "timeStamp": date.today(),
#                 },
#             ],
#             ratings_json,
#         )
#
#     def test_get_ratings_by_creatorid(self):
#         ratings = get_ratings_by_creator(2)
#         self.assertListEqual(
#             ratings,
#             [
#                 {
#                     "id": 2,
#                     "creatorId": 2,
#                     "targetId": 1,
#                     "score": 4,
#                     "timeStamp": date.today(),
#                 }
#             ],
#         )
#
#     def test_get_ratings_by_targetid(self):
#         ratings = get_ratings_by_target(2)
#         self.assertListEqual(
#             ratings,
#             [
#                 {
#                     "id": 1,
#                     "creatorId": 1,
#                     "targetId": 2,
#                     "score": 3,
#                     "timeStamp": date.today(),
#                 }
#             ],
#         )
#
#     def test_get_rating_by_actors(self):
#         rating = get_rating_by_actors(1, 2)
#         assert rating.id == 1
#
#     def test_update_rating(self):
#         rating = update_rating(1, 5)
#         assert rating.score == 5
#
#     def test_try_calculate_rating(self):
#         user = create_user("phil", "philpass")
#         rating = create_rating(user.id, 2, 5)
#         calculated = get_calculated_rating(2)
#         assert calculated == 4
#
#     def test_get_level(self):
#         assert get_level(1) == 1
#
#
# class RankingIntegrationTests(unittest.TestCase):
#     def test_create_rating(self):
#         ranking = create_ranking(1, 2, 3)
#         assert ranking.id == 1
#
#     def test_get_ranking(self):
#         ranking = get_ranking(1)
#         assert ranking.creatorId == 1
#
#     def test_get_all_rankings(self):
#         ranking = create_ranking(2, 1, 4)
#         rankingList = []
#         rankingList.append(get_ranking(1))
#         rankingList.append(get_ranking(2))
#         self.assertListEqual(get_all_rankings(), rankingList)
#
#     def test_get_all_rankings_json(self):
#         rankings_json = get_all_rankings_json()
#         self.assertListEqual(
#             [
#                 {"id": 1, "creatorId": 1, "imageId": 2, "score": 3},
#                 {"id": 2, "creatorId": 2, "imageId": 1, "score": 4},
#             ],
#             rankings_json,
#         )
#
#     def test_get_rankings_by_creatorid(self):
#         rankings = get_rankings_by_creator(2)
#         self.assertListEqual(
#             rankings, [{"id": 2, "creatorId": 2, "imageId": 1, "score": 4}]
#         )
#
#     def test_get_rankings_by_imageid(self):
#         rankings = get_rankings_by_image(2)
#         self.assertListEqual(
#             rankings, [{"id": 1, "creatorId": 1, "imageId": 2, "score": 3}]
#         )
#
#     def test_get_ranking_by_actors(self):
#         ranking = get_ranking_by_actors(1, 2)
#         assert ranking.id == 1
#
#     def test_update_ranking(self):
#         ranking = update_ranking(1, 5)
#         assert ranking.score == 5
#
#     def test_try_calculate_ranking(self):
#         ranking = create_ranking(3, 2, 5)
#         calculated = get_calculated_ranking(2)
#         assert calculated == 4
