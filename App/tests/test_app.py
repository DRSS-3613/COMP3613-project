import os, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify
from datetime import date, datetime

from App.database import create_db
from App.models import User, Image, Rating, Ranking, Feed, Distributor

from App.controllers.user import (create_user)
from App.controllers.image import (create_image)
from App.controllers.feed import (create_feed)
from App.controllers.rating import (create_rating)
from App.controllers.ranking import (create_ranking)
from App.controllers.distributor import (create_distributor)

# from App.controllers import (
#     create_user,
#     get_user,
#     get_user_by_username,
#     get_all_users,
#     get_all_users_json,
#     update_user,
#     delete_user,
#     create_image,
#     get_all_images,
#     get_all_images_json,
#     get_images_by_userid_json,
#     get_image,
#     get_image_json,
#     delete_image,
#     create_rating,
#     get_all_ratings,
#     get_all_ratings_json,
#     get_rating,
#     get_ratings_by_target,
#     get_ratings_by_creator,
#     get_rating_by_actors,
#     update_rating,
#     get_calculated_rating,
#     get_level,
#     create_ranking,
#     get_all_rankings,
#     get_all_rankings_json,
#     get_ranking,
#     get_rankings_by_image,
#     get_rankings_by_creator,
#     get_ranking_by_actors,
#     get_calculated_ranking,
#     update_ranking,
#     authenticate,
# )

from wsgi import app

LOGGER = logging.getLogger(__name__)

"""
   Unit Tests
"""


class UserUnitTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("bob", "bobpass")
        self.assertEqual(user.username, "bob")

    def test_to_json(self):
        user = User("bob", "bobpass")
        user_json = user.to_json()
        self.assertDictEqual(
            user_json, {"id": None, "username": "bob", "images": [], "ratings": []}
        )

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method="sha256")
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
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
        rank1 = Ranking(2, image.id, 5)
        rank2 = Ranking(3, image.id, 1)
        assert image.get_average_rank() == 3

    def test_get_rankings(self):
        image = Image(1, "https://www.picsum.com/200/300")
        rank1 = Ranking(2, image.id, 1)
        assert image.get_rankings() == [rank1]


class RatingUnitTests(unittest.TestCase):
    def test_new_rating(self):
        rating = Rating(1, 2, 3)
        assert rating.score == 3

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
        assert ranking.score == 3

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




# """
#     Integration Tests
# """
#
# # This fixture creates an empty database for the test and deletes it after the test
# # scope="class" would execute the fixture once and resued for all methods in the class
# @pytest.fixture(autouse=True, scope="module")
# def empty_db():
#     app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"})
#     create_db(app)
#     yield app.test_client()
#     os.unlink(os.getcwd() + "/App/test.db")
#
#
# def test_authenticate():
#     user = create_user("bob", "bobpass")
#     assert authenticate("bob", "bobpass") != None
#
#
# class UsersIntegrationTests(unittest.TestCase):
#     def test_create_user(self):
#         user = create_user("rick", "bobpass")
#         assert user.username == "rick"
#
#     def test_get_user(self):
#         user = get_user(1)
#         assert user.username == "bob"
#
#     def test_get_user_by_username(self):
#         user = get_user_by_username("rick")
#         assert user["username"] == "rick"
#
#     def test_get_all_users(self):
#         userList = []
#         userList.append(get_user(1))
#         userList.append(get_user(2))
#         self.assertEqual(get_all_users(), userList)
#
#     def test_get_all_users_json(self):
#         users_json = get_all_users_json()
#         self.assertListEqual(
#             [
#                 {"id": 1, "username": "bob", "images": [], "ratings": []},
#                 {"id": 2, "username": "rick", "images": [], "ratings": []},
#             ],
#             users_json,
#         )
#
#     def test_update_user(self):
#         update_user(1, "ronnie")
#         user = get_user(1)
#         assert user.username == "ronnie"
#
#     def test_delete_user(self):
#         create_user("phil", "philpass")
#         delete_user(3)
#         user = get_user(3)
#         assert user == None
#
#
# class ImageIntegrationTests(unittest.TestCase):
#     def test_create_image(self):
#         image = create_image(2)
#         assert image.id == 1
#
#     def test_get_image(self):
#         image = get_image(1)
#         assert image.userId == 2
#
#     def test_get_all_images(self):
#         image = create_image(1)
#         imageList = []
#         imageList.append(get_image(1))
#         imageList.append(get_image(2))
#         self.assertListEqual(get_all_images(), imageList)
#
#     def test_get_all_images_json(self):
#         images_json = get_all_images_json()
#         self.assertListEqual(
#             [
#                 {"id": 1, "rankings": [], "userId": 2},
#                 {"id": 2, "rankings": [], "userId": 1},
#             ],
#             images_json,
#         )
#
#     def test_get_images_by_userid_json(self):
#         images_json = get_images_by_userid_json(2)
#         self.assertListEqual(images_json, [{"id": 1, "rankings": [], "userId": 2}])
#
#     def test_delete_image(self):
#         image = create_image(1)
#         delete_image(image.id)
#         image = get_image(image.id)
#         assert image == None
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
