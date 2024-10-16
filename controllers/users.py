from flask import jsonify, request
from repositories.repository_factory import users_repository_factory


def get_all_users():
    try:
        # .env-tiedostossa määritellystä tietokannasta riippuen repo-muuttujaan
        # haetaan joko UsersRepositoryMySQL()- tai
        # UsersRepositoryPostgres()-instanssi:
        repo = users_repository_factory()
        # Haetaan instanssin metodin palauttama lista users-muuttujaan:
        users = repo.get_all()

        # Muutetaan listan sisällään pitämät User-luokan instanssit
        # dictionaryiksi:
        user_dict_list = [{"id": user.id,
                           "username": user.username,
                           "firstname": user.firstname,
                           "lastname": user.lastname}
                          for user in users]

        # Muutetaan lista dictionary-alkioineen json-muotoon ja palautetaan se:
        return jsonify(user_dict_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_user_by_id(user_id):
    try:
        repo = users_repository_factory()
        # repo-muuttujassa olevan instanssin jäsenmetodia hyödyntämällä
        # haetaan user-muuttujaan User-luokan instanssi id:n perusteella:
        user = repo.get_by_id(user_id)

        # Jos käyttäjää ei löydy haetulla id:llä, palataan funktiosta
        # json-muotoisella virheviestillä:
        if user is None:
            return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

        # Muussa tapauksessa tehdään käyttäjäinstanssin tiedoista dictionary:
        user_dict = {"id": user.id,
                     "username": user.username,
                     "firstname": user.firstname,
                     "lastname": user.lastname}

        # Muutetaan dictionary json-muotoon ja palautetaan se:
        return jsonify(user_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_user():
    try:
        # Haetaan bodyssa saatavat tiedot request_data-muuttujaan Flaskin
        # request-ominaisuuden get_json()-metodia hyödyntämällä.
        request_data = request.get_json()
        username = request_data.get("username")
        firstname = request_data.get("firstname")
        lastname = request_data.get("lastname")

        # Jos request bodysta puuttuu yksi tai useampi tietokantahakua
        # varten tarvittava avain-arvo-pari, palataan funktiosta
        # json-muotoisella virheviestillä:
        if not username or not firstname or not lastname:
            return jsonify({"error": "Vääränlainen request body"}), 400

        repo = users_repository_factory()
        # Talletetaan added_user-muuttujaan add-metodin palauttama
        # instanssi. Metodille välitetään bodysta saatavien avainten arvot.
        # Metodi lisää käyttäjän tietokantaan näillä tiedoilla.
        added_user = repo.add(username, firstname, lastname)

        # Jos käyttäjäinstanssin id indikoi epäonnistuneesta
        # tietokantaoperaatiosta, poistutaan funktiosta virheestä kertovalla
        # json-viestillä:
        if added_user.id < 1:
            return jsonify({"error": "Käyttäjän lisääminen ei onnistu"}), 500

        added_user_dict = {"id": added_user.id,
                           "username": added_user.username,
                           "firstname": added_user.firstname,
                           "lastname": added_user.lastname}

        return jsonify(added_user_dict), 201

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
        # Talletetaan updated_user-muuttujaan update_by_id-metodin palauttama
        # User-luokan instanssi. Metodille välitetään saatu id sekä bodysta
        # saatavien avainten arvot. Metodi päivittää käyttäjän tiedot
        # välitetyillä arvoilla välitetyn id:n perusteella.
        updated_user = repo.update_by_id(user_id, username, firstname, lastname)

        if updated_user is None:
            return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

        updated_user_dict = {"id": updated_user.id,
                             "username": updated_user.username,
                             "firstname": updated_user.firstname,
                             "lastname": updated_user.lastname}

        return jsonify(updated_user_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_user_lastname_by_id(user_id):
    try:
        request_data = request.get_json()
        lastname = request_data.get("lastname")

        if not lastname:
            return jsonify({"error": "Vääränlainen request body"}), 400

        repo = users_repository_factory()
        # Talletetaan updated_user-muuttujaan update_lastname_by_id-metodin
        # palauttama User-luokan instanssi. Metodille välitetään saatu id sekä
        # bodysta saatavan avaimen arvo. Metodi päivittää käyttäjän sukunimen
        # välitetyllä arvolla välitetyn id:n perusteella.
        updated_user = repo.update_lastname_by_id(user_id, lastname)

        if updated_user is None:
            return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

        updated_user_dict = {"id": updated_user.id,
                             "username": updated_user.username,
                             "firstname": updated_user.firstname,
                             "lastname": updated_user.lastname}

        return jsonify(updated_user_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_user_by_id(user_id):
    try:
        repo = users_repository_factory()
        # Talletetaan removed_user-muuttujaan delete_by_id-metodin palauttama
        # User-luokan instanssi. Metodille välitetään saatu id, jonka
        # perusteella käyttäjä poistetaan.
        removed_user = repo.delete_by_id(user_id)

        if removed_user is None:
            return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404

        # Jos käyttäjän poistaminen onnistuu, palautetaan funktiosta vastaus.
        # Ei palauteta poistetun käyttäjän tietoja, koska käyttäjä on
        # poistettu.
        return jsonify({"response": f"Käyttäjä id:llä {removed_user.id} poistettu."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
