from App.models import Ranking
from App.database import db


def create_ranking(ranker_id, image_id, rank):
    ranking = Ranking(ranker_id, image_id, rank)
    db.session.add(ranking)
    db.session.commit()
    return ranking


def get_ranking(id):
    ranking = Ranking.query.get(id)
    return ranking


def get_ranking_json(id):
    ranking = Ranking.query.get(id)
    return ranking.to_json()


def get_all_rankings():
    rankings = Ranking.query.all()
    return rankings


def get_all_rankings_json():
    rankings = Ranking.query.all()
    return [ranking.to_json() for ranking in rankings]


def get_rankings_by_ranker(ranker_id):
    rankings = Ranking.query.filter_by(ranker_id=ranker_id).all()
    return rankings


def get_rankings_by_ranker_json(ranker_id):
    rankings = Ranking.query.filter_by(ranker_id=ranker_id).all()
    return [ranking.to_json() for ranking in rankings]


def get_rankings_by_image(image_id):
    rankings = Ranking.query.filter_by(image_id=image_id).all()
    return rankings


def get_rankings_by_image_json(image_id):
    rankings = Ranking.query.filter_by(image_id=image_id).all()
    return [ranking.to_json() for ranking in rankings]


def update_ranking(id, rank):
    ranking = Ranking.query.get(id)
    if ranking:
        ranking.rank = rank
        db.session.commit()
        return ranking
    return None


def delete_ranking(id):
    ranking = Ranking.query.get(id)
    if ranking:
        db.session.delete(ranking)
        return db.session.commit()
    return None
