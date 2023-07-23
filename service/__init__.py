from flask import Flask, render_template
from webargs.flaskparser import use_args
from flask_socketio import join_room
from flask_socketio import SocketIO
from webargs import fields
from flask import request
import config

callback_args = {
    "signature": fields.Str(required=True),
    "address": fields.Str(required=True),
}


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret
    socketio = SocketIO(app, cors_allowed_origins="*")

    with app.app_context():

        @app.route("/")
        def index():
            return render_template("index.html")

        @app.route("/app.json")
        def app_json():
            return {"name": config.name, "icon": config.icon}

        @app.route("/call/<string:session>", methods=["POST"])
        @use_args(callback_args, location="json")
        def call(args, session):
            socketio.emit(session, args, to=session)
            return {"status": "success"}

        @socketio.on("callback")
        def callback(session, *args):
            join_room(session, request.sid)
            return True

        return app
