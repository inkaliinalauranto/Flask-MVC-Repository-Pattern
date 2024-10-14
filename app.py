from dotenv import load_dotenv
from flask import Flask

from controllers.users import get_all_users

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.add_url_rule(rule="/api/users", view_func=get_all_users)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
