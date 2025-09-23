from flask import Flask
from flask_session import Session


from .auth.routes import auth
from .dashboard.routes import dashboard
from .weather.routes import weather
from config import Config

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    Session(app)

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(weather)

    return app
