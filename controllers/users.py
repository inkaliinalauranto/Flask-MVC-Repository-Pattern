from flask import jsonify, request
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


def add_user():
    request_data = request.get_json()
    repo = users_repository_factory()
    added_user = repo.add(request_data.get("username"), request_data.get("firstname"), request_data.get("lastname"))

    if added_user.id < 1:
        return jsonify({"error": "Käyttäjän lisääminen ei onnistu"}), 500

    return jsonify({"response": f"Käyttäjä lisätty id:llä {added_user.id}."}), 201
