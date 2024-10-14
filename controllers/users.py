from flask import jsonify
from repositories.repository_factory import users_repository_factory


def get_all_users():
    repo = users_repository_factory()
    users = repo.get_all()
    user_dict_list = [{"id": user.id,
                       "username": user.username,
                       "firstname": user.firstname,
                       "lastname": user.lastname}
                      for user in users]

    return jsonify(user_dict_list)


def get_user_by_id(user_id):
    repo = users_repository_factory()
    user = repo.get_by_id(user_id)
    user_dict = {"id": user.id,
                 "username": user.username,
                 "firstname": user.firstname,
                 "lastname": user.lastname}

    return user_dict
