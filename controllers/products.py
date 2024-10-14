from repositories.repository_factory import products_repository_factory
from flask import jsonify


def get_all_products():
    repo = products_repository_factory()
    products = repo.get_all()
    product_dict_list = [{"id": product.id,
                          "name": product.name,
                          "description": product.description}
                         for product in products]

    return jsonify(product_dict_list)
