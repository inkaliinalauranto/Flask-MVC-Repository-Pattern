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

    if not user:
        return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

    user_dict = {"id": user.id,
                 "username": user.username,
                 "firstname": user.firstname,
                 "lastname": user.lastname}

    return user_dict


def add_user():
    request_data = request.get_json()
    username = request_data.get("username")
    firstname = request_data.get("firstname")
    lastname = request_data.get("lastname")

    if not username or not firstname or not lastname:
        return jsonify({"error": "Vääränlainen request body"}), 400

    repo = users_repository_factory()
    added_user = repo.add(username, firstname, lastname)

    if added_user.id < 1:
        return jsonify({"error": "Käyttäjän lisääminen ei onnistu"}), 500

    return jsonify({"response": f"Käyttäjä lisätty id:llä {added_user.id}."}), 201


def update_user_by_id(user_id):
    repo = users_repository_factory()
    user = repo.get_by_id(user_id)

    if not user:
        return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

    request_data = request.get_json()
    username = request_data.get("username")
    firstname = request_data.get("firstname")
    lastname = request_data.get("lastname")

    if not username or not firstname or not lastname:
        return jsonify({"error": "Vääränlainen request body"}), 400

    updated_user = repo.update_by_id(user_id, username, firstname, lastname)
    return jsonify({"response": f"Käyttäjän (id: {updated_user.id}) tietoja muokattu."})


def update_user_lastname_by_id(user_id):
    repo = users_repository_factory()
    user = repo.get_by_id(user_id)

    if not user:
        return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

    request_data = request.get_json()
    lastname = request_data.get("lastname")

    if not lastname:
        return jsonify({"error": "Vääränlainen request body"}), 400

    updated_user = repo.update_by_id(user_id, user.username, user.firstname, lastname)
    return jsonify({"response": f"Käyttäjän (id: {updated_user.id}) sukunimeä muokattu."})


def delete_by_id(user_id):
    repo = users_repository_factory()
    user = repo.get_by_id(user_id)

    if not user:
        return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

    removed_user = repo.delete_by_id(user_id, user.username, user.firstname, user.lastname)
    return jsonify({"response": f"Käyttäjä id:llä {removed_user.id} poistettu."})
