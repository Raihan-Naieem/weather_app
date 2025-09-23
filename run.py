from app import create_app
from app.util import SQL

app = create_app()

if __name__ == '__main__':

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
    app.run(host='0.0.0.0', port=5000, debug=True)    
