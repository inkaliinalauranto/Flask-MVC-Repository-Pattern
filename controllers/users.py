from flask import jsonify
from repositories.repository_factory import users_repository_factory


def get_all_users():
    repo = users_repository_factory()
    users = repo.get_all()
    users_json = [{"id": user.id,
                   "username": user.username,
                   "firstname": user.firstname,
                   "lastname": user.lastname}
                  for user in users]

    return jsonify(users_json)
