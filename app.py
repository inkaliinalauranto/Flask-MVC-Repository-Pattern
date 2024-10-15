from flask import Flask
from controllers.users import get_all_users, get_user_by_id, add_user, update_user_by_id
from controllers.products import get_all_products
from dotenv import load_dotenv

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.add_url_rule(rule="/api/users", view_func=get_all_users)
app.add_url_rule(rule="/api/users/<int:user_id>", view_func=get_user_by_id)
app.add_url_rule(rule="/api/users",
                 view_func=add_user,
                 methods=["POST"])
app.add_url_rule(rule="/api/users/<int:user_id>", view_func=update_user_by_id, methods=["PUT"])

app.add_url_rule(rule="/api/products", view_func=get_all_products)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
