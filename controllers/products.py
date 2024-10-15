from repositories.repository_factory import products_repository_factory
from flask import jsonify, request


def get_all_products():
    repo = products_repository_factory()
    products = repo.get_all()
    product_dict_list = [{"id": product.id,
                          "name": product.name,
                          "description": product.description}
                         for product in products]

    return jsonify(product_dict_list)


def get_product_by_id(product_id):
    try:
        repo = products_repository_factory()
        product = repo.get_by_id(product_id)

        if product is None:
            return jsonify({"error": f"Tuotetta id:llä {product_id} ei ole olemassa."}), 404

        product_dict = {"id": product.id,
                        "name": product.name,
                        "description": product.description}

        return jsonify(product_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_product():
    try:
        request_data = request.get_json()
        name = request_data.get("name")
        description = request_data.get("description")

        if not name or not description:
            return jsonify({"error": "Vääränlainen request body"}), 400

        repo = products_repository_factory()
        added_product = repo.add(name, description)

        if added_product.id < 1:
            return jsonify({"error": "Tuotteen lisääminen ei onnistu"}), 500

        return jsonify({"response": f"Tuote lisätty id:llä {added_product.id}."}), 201

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
        updated_product = repo.update_by_id(product_id, name, description)

        if updated_product is None:
            return jsonify({"error": f"Tuotetta id:llä {product_id} ei ole olemassa."}), 404

        return jsonify({"response": f"Tuotteen (id: {updated_product.id}) tietoja muokattu."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_product_description_by_id(product_id):
    try:
        request_data = request.get_json()
        description = request_data.get("description")

        if not description:
            return jsonify({"error": "Vääränlainen request body"}), 400

        repo = products_repository_factory()
        updated_product = repo.update_description_by_id(product_id, description)

        if updated_product is None:
            return jsonify({"error": f"Tuotetta id:llä {product_id} ei ole olemassa."}), 404

        return jsonify({"response": f"Tuotteen (id: {updated_product.id}) kuvausta muokattu."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_product_by_id(product_id):
    try:
        repo = products_repository_factory()
        removed_product = repo.delete_by_id(product_id)

        if removed_product is None:
            return jsonify({"error": f"Tuotetta id:llä {product_id} ei ole olemassa."}), 404

        return jsonify({"response": f"Tuote id:llä {removed_product.id} poistettu."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
