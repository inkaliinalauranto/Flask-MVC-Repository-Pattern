from flask import Flask
from controllers.users import get_all_users, get_user_by_id, add_user, update_user_by_id, update_user_lastname_by_id, \
    delete_user_by_id
from controllers.products import get_all_products, add_product, update_product_by_id, update_product_description_by_id, \
    delete_product_by_id, get_product_by_id
from dotenv import load_dotenv

app = Flask(__name__)

# User ////////////////////////////////////////////////////////////////////////
app.add_url_rule(rule="/api/users", view_func=get_all_users)

# Path-parametrin käsittely on toteutettu seuraavasta lähteestä löytyvän
# esimerkin mukaan:
# https://www.geeksforgeeks.org/flask-app-routing/
app.add_url_rule(rule="/api/users/<int:user_id>", view_func=get_user_by_id)

# Halutun HTTP-metodin määrittely add_url_rule-metodin methods-parametrina
# listan sisään asetettuna merkkijonona on toteutettu seuraavasta osoitteesta
# löytyvän ehdotuksen mukaan:
# https://stackoverflow.com/questions/15421193/using-defaults-with-app-add-url-rule-in-flask
app.add_url_rule(rule="/api/users",
                 view_func=add_user,
                 methods=["POST"])

app.add_url_rule(rule="/api/users/<int:user_id>",
                 view_func=update_user_by_id,
                 methods=["PUT"])

app.add_url_rule(rule="/api/users/<int:user_id>",
                 view_func=update_user_lastname_by_id,
                 methods=["PATCH"])

app.add_url_rule(rule="/api/users/<int:user_id>",
                 view_func=delete_user_by_id,
                 methods=["DELETE"])
# /////////////////////////////////////////////////////////////////////////////

# Product /////////////////////////////////////////////////////////////////////
app.add_url_rule(rule="/api/products", view_func=get_all_products)

app.add_url_rule(rule="/api/products/<int:product_id>", view_func=get_product_by_id)

app.add_url_rule(rule="/api/products",
                 view_func=add_product,
                 methods=["POST"])

app.add_url_rule(rule="/api/products/<int:product_id>",
                 view_func=update_product_by_id,
                 methods=["PUT"])

app.add_url_rule(rule="/api/products/<int:product_id>",
                 view_func=update_product_description_by_id,
                 methods=["PATCH"])

app.add_url_rule(rule="/api/products/<int:product_id>",
                 view_func=delete_product_by_id,
                 methods=["DELETE"])
# /////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    load_dotenv()
    # debug-parametrin käyttö palvelimen uudelleen käynnistämiseksi
    # automaattisesti koodimuutosten yhteydessä on toteutettu seuraavasta
    # lähteestä löytyvän mallin mukaan:
    # https://www.geeksforgeeks.org/flask-app-routing/
    app.run(debug=True)
