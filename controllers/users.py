from flask import jsonify, request
from repositories.repository_factory import users_repository_factory


def get_all_users():
    try:
        repo = users_repository_factory()
        users = repo.get_all()

        user_dict_list = [{"id": user.id,
                           "username": user.username,
                           "firstname": user.firstname,
                           "lastname": user.lastname}
                          for user in users]

        return jsonify(user_dict_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_user_by_id(user_id):
    try:
        repo = users_repository_factory()
        user = repo.get_by_id(user_id)

        if user is None:
            return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

        user_dict = {"id": user.id,
                     "username": user.username,
                     "firstname": user.firstname,
                     "lastname": user.lastname}

        return jsonify(user_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_user():
    try:
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_user_by_id(user_id):
    try:
        request_data = request.get_json()
        username = request_data.get("username")
        firstname = request_data.get("firstname")
        lastname = request_data.get("lastname")

        if not username or not firstname or not lastname:
            return jsonify({"error": "Vääränlainen request body"}), 400

        repo = users_repository_factory()
        updated_user = repo.update_by_id(user_id, username, firstname, lastname)

        if updated_user is None:
            return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

        return jsonify({"response": f"Käyttäjän (id: {updated_user.id}) tietoja muokattu."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_user_lastname_by_id(user_id):
    try:
        request_data = request.get_json()
        lastname = request_data.get("lastname")

        if not lastname:
            return jsonify({"error": "Vääränlainen request body"}), 400

        repo = users_repository_factory()
        updated_user = repo.update_by_id(user_id, lastname)

        if updated_user is None:
            return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

        return jsonify({"response": f"Käyttäjän (id: {updated_user.id}) sukunimeä muokattu."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_by_id(user_id):
    try:
        repo = users_repository_factory()
        removed_user = repo.delete_by_id(user_id)

        if removed_user is None:
            return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

        return jsonify({"response": f"Käyttäjä id:llä {removed_user.id} poistettu."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

