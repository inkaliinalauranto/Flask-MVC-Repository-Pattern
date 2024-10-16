from repositories.repository_factory import products_repository_factory
from flask import jsonify, request


def get_all_products():
    try:
        # .env-tiedostossa määritellystä tietokannasta riippuen repo-muuttujaan
        # haetaan joko UsersRepositoryMySQL()- tai
        # UsersRepositoryPostgres()-instanssi:
        repo = products_repository_factory()
        # Haetaan instanssin metodin palauttama lista products-muuttujaan:
        products = repo.get_all()
        # Muutetaan listan sisällään pitämät Product-luokan instanssit
        # dictionaryiksi:
        product_dict_list = [{"id": product.id,
                              "name": product.name,
                              "description": product.description}
                             for product in products]

        # Muutetaan lista dictionary-alkioineen json-muotoon ja palautetaan se:
        return jsonify(product_dict_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_product_by_id(product_id):
    try:
        repo = products_repository_factory()
        # repo-muuttujassa olevan instanssin jäsenmetodia hyödyntämällä
        # haetaan product-muuttujaan Product-luokan instanssi id:n perusteella:
        product = repo.get_by_id(product_id)

        # Jos tuotetta ei löydy haetulla id:llä, palataan funktiosta
        # json-muotoisella virheviestillä:
        if product is None:
            return jsonify({"error": f"Tuotetta id:llä {product_id} ei ole olemassa."}), 404

        # Muussa tapauksessa tehdään tuoteinstanssin tiedoista dictionary:
        product_dict = {"id": product.id,
                        "name": product.name,
                        "description": product.description}

        # Muutetaan dictionary json-muotoon ja palautetaan se:
        return jsonify(product_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_product():
    try:
        # Haetaan bodyssa saatavat tiedot request_data-muuttujaan Flaskin
        # request-ominaisuuden get_json()-metodia hyödyntämällä.
        request_data = request.get_json()
        name = request_data.get("name")
        description = request_data.get("description")

        # Jos request bodysta puuttuu yksi tai useampi tietokantahakua
        # varten tarvittava avain-arvo-pari, palataan funktiosta
        # json-muotoisella virheviestillä:
        if not name or not description:
            return jsonify({"error": "Vääränlainen request body"}), 400

        repo = products_repository_factory()
        # Talletetaan added_product-muuttujaan add-metodin palauttama
        # instanssi. Metodille välitetään bodysta saatavien avainten arvot.
        # Metodi lisää tuotteen tietokantaan näillä tiedoilla.
        added_product = repo.add(name, description)

        # Jos tuoteinstanssin id indikoi epäonnistuneesta
        # tietokantaoperaatiosta, poistutaan funktiosta virheestä kertovalla
        # json-viestillä:
        if added_product.id < 1:
            return jsonify({"error": "Tuotteen lisääminen ei onnistu"}), 500

        added_product_dict = {"id": added_product.id,
                              "name": added_product.name,
                              "description": added_product.description}

        return jsonify(added_product_dict), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_product_by_id(product_id):
    try:
        request_data = request.get_json()
        name = request_data.get("name")
        description = request_data.get("description")

        if not name or not description:
            return jsonify({"error": "Vääränlainen request body"}), 400

        repo = products_repository_factory()
        # Talletetaan updated_product-muuttujaan update_by_id-metodin
        # palauttama Product-luokan instanssi. Metodille välitetään saatu id
        # sekä bodysta saatavien avainten arvot. Metodi päivittää tuotteen
        # tiedot välitetyillä arvoilla välitetyn id:n perusteella.
        updated_product = repo.update_by_id(product_id, name, description)

        if updated_product is None:
            return jsonify({"error": f"Tuotetta id:llä {product_id} ei ole olemassa."}), 404

        updated_product_dict = {"id": updated_product.id,
                                "name": updated_product.name,
                                "description": updated_product.description}

        return jsonify(updated_product_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_product_description_by_id(product_id):
    try:
        request_data = request.get_json()
        description = request_data.get("description")

        if not description:
            return jsonify({"error": "Vääränlainen request body"}), 400

        repo = products_repository_factory()
        # Talletetaan updated_product-muuttujaan
        # update_description_by_id-metodin palauttama Product-luokan
        # instanssi. Metodille välitetään saatu id sekä bodysta saatavan
        # avaimen arvo. Metodi päivittää tuotteen kuvauksen välitetyllä
        # arvolla välitetyn id:n perusteella.
        updated_product = repo.update_description_by_id(product_id, description)

        if updated_product is None:
            return jsonify({"error": f"Tuotetta id:llä {product_id} ei ole olemassa."}), 404

        updated_product_dict = {"id": updated_product.id,
                                "name": updated_product.name,
                                "description": updated_product.description}

        return jsonify(updated_product_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_product_by_id(product_id):
    try:
        repo = products_repository_factory()
        # Talletetaan removed_product-muuttujaan delete_by_id-metodin
        # palauttama Product-luokan instanssi. Metodille välitetään saatu id,
        # jonka perusteella tuote poistetaan.
        removed_product = repo.delete_by_id(product_id)

        if removed_product is None:
            return jsonify({"error": f"Tuotetta id:llä {product_id} ei ole olemassa."}), 404

        # Jos tuotteen poistaminen onnistuu, palautetaan funktiosta vastaus.
        # Ei palauteta poistetun tuotteen tietoja, koska tuotehan on poistettu.
        return jsonify({"response": f"Tuote id:llä {removed_product.id} poistettu."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
