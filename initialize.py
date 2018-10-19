import flask
from flask_restful import Api


def create_app():
    app = flask.Flask(__name__)
    api = Api(app)
    return app, api


app, api = create_app()