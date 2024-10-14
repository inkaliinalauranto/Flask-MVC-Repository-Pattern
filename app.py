from flask import Flask
from controllers.users import get_all_users
from controllers.products import get_all_products
from dotenv import load_dotenv

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.add_url_rule(rule="/api/users", view_func=get_all_users)
app.add_url_rule(rule="/api/products", view_func=get_all_products)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
