from flask import Flask, render_template
from flask_socketio import join_room
from flask_socketio import SocketIO
from flask import request
import config


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
        def call(session):
            socketio.emit(session, request.json, to=session)
            return {"status": "success"}

        @socketio.on("callback")
        def callback(session, *args):
            join_room(session, request.sid)
            return True

        return app
