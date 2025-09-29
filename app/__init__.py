from flask import Flask
from flask_session import Session
from .util import SQL



from .errors import errors
from .auth.routes import auth
from .dashboard.routes import dashboard
from .weather.routes import weather
from config import Config

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    Session(app)

    app.register_blueprint(errors)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(weather)

    with app.app_context():
        SQL(
        '''
         CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            email VARCHAR(50) NOT NULL UNIQUE, 
            password_hash VARCHAR(255) NOT NULL,
            country_code VARCHAR(20) NULL
         );
        '''
        )

        # add user id foreign key
        SQL(
        '''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            country_code TEXT NOT NULL,
            city TEXT NOT NULL,
            status TEXT NOT NULL,
            temperature REAL NOT NULL,
            windspeed REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        '''
        )

    return app

create_app = create_app()
