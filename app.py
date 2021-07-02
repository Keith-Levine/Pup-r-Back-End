from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

import boto3
s3 = boto3.resource('s3')

import models
from resources.dogs import dog
from resources.user import user
# from resources.likes import likes

login_manager = LoginManager()

DEBUG = True
PORT = 5000

app = Flask(__name__)


app.secret_key = 'TopSecretDoNotSteal'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return jsonify(app="Connected")

# CORS is a class from the flask_cors package that will allows cors connections
# param 1: The Blueprint we want to allow cors connections on
# param 2: The origins we allow cors connections from
# param 3: Allow login from those origins
CORS(dog, origins=['http://localhost:3000'], supports_credentials=True)
# Actually connect the routes in a Blueprint to the flask app
# param 1: The Blueprint we are registering
# param 2: The prefix that all Blueprint routes will be preceeded by
app.register_blueprint(dog, url_prefix='/api/v1/dogs')


CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/users')

# CORS(likes, origins=['http://localhost:3000'], supports_credentials=True)
# app.register_blueprint(user, url_prefix='/api/v1/likes')

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)