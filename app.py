
from typing import Any
from collections import defaultdict
import requests
from flask import  Flask, request, redirect, render_template, session, url_for, flash 
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv
import os

load_dotenv()



from util import SQL, login_required, get_country_codes, get_cities

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')



# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_PERMANENT'] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)


API_KEY = os.getenv('OpenWeather_API_KEY')


# AUTH
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password")

        country_code = request.form.get("country_code")
        if not country_code:
            return "country code not found", 404
        country_codes: list[str] = get_country_codes()

        if country_code.upper() not in country_codes:
            flash("Invalid country code!", "danger")
            return render_template("register.html", navbar=False, country_codes= country_codes)
        # confirms password
        if not password == confirm_password:
            flash("Password Mismatch", "danger")
            return render_template("register.html", navbar=False, country_codes= country_codes)
        
        password_hash = generate_password_hash(password)

        # error if sql aint sqling
        try:
            SQL("INSERT INTO users (email, password_hash, country_code) VALUES (?, ?, ?)", email, password_hash, country_code)
        except ValueError as error:
            flash(str(error), 'danger')
            return redirect(url_for('register'))
        
        # Returns a list of one dict where email is matched
        rows: list[dict[Any,Any]] = SQL("SELECT * FROM users WHERE email = ? ", email) or []

        # Remember user id session
        session["user_id"] = rows[0]["id"]
        session['email'] = rows[0]['email']

        flash('Registered successfully!', 'success')
        return redirect(url_for("login"))
    
    elif request.method == "GET":
        # to give user a drop down box of country codes to select from
        country_codes = get_country_codes()
        return render_template("register.html", navbar=False, country_codes= country_codes)

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        rows: list[dict[Any,Any]] = SQL("SELECT * FROM users WHERE email = ?", email) or []

        # if no user data in database
        if len(rows) != 1 :
            flash("email not found!", "danger")
            return render_template("login.html",navbar=False)

            

        password_hash_from_db: str = rows[0]["password_hash"]

        is_password_valid = check_password_hash(password_hash_from_db, password or "")

        if not is_password_valid:
            flash("Invalid Password!", "danger")
            return render_template("login.html",navbar=False)


        # to remember user
        session["user_id"] = rows[0]["id"]
        session['email'] = rows[0]['email']
        flash("Logged in succesefully!", "success")
        return redirect(url_for("index"))
    elif request.method == "GET":
        return render_template("login.html",navbar=False)


@app.route("/logout", methods=["GET"])
def logout():

    session.clear()
    flash('Logged out!', 'danger') 
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # TODO: 
    # will show country code and a option to change them
    # will show added city with pagination and can delete
    # some basic data manipulation (ex highest temp, avg temp etc)

    if request.method == "GET":
        weather_data_set: list[dict] = SQL('''
            SELECT
                id,
                country_code, 
                city,
                status, 
                temperature, 
                windspeed, 
                timestamp 
            FROM weather_data 
            WHERE user_id = ?
            ''', session["user_id"]) or []
        if not weather_data_set:
            flash("No weather data found! Please search and add a city first.", "warning")
            return redirect(url_for('search_city_info'))

        rows: list[dict] = SQL("SELECT country_code FROM users WHERE id = ?", session["user_id"]) or []
        current_country_code = rows[0]["country_code"].upper()


        return render_template("index.html", weather_data_set=weather_data_set, current_country_code=current_country_code ,available_codes=get_country_codes())

@app.route("/delete_row", methods=["POST"])
def delete_row():
    id = request.args.get('id', type=int)
    if not id:
        flash("Deletion error!")
        return redirect(url_for("index"))
    SQL('''
        DELETE FROM weather_data 
        WHERE id = ? AND 
        user_id = ?
        ''', id, session["user_id"])
    return redirect(url_for("index"))


@app.route("/update_country_code", methods=["POST"])
def update_country_code():
    update_code = request.form.get("country_code", "").strip().upper()
    available_codes = get_country_codes()

    if not update_code:
        flash("Country code cannot be empty!", "danger")
        return redirect(url_for("index"))

    if update_code not in available_codes:
        flash("Invalid updated country code!", "danger")
        return redirect(url_for("index"))

    SQL('''
        UPDATE users 
        SET country_code = ? 
        WHERE id = ?
        ''', update_code, session["user_id"])
    flash("Country code updated!", "success")
    return redirect(url_for("index"))



    

@app.route("/search_city_info", methods=["GET","POST"])
def search_city_info():
    if request.method == "POST":
        city: str = request.form.get("city", "")
        if not city:
            flash("Enter a valid city name!", "danger")
            return redirect("search_city_info")
        return redirect(url_for("show_city_info", city=city))
            
    elif request.method == "GET":       
        id = session['user_id']
        rows: list[dict] = SQL("SELECT country_code FROM users WHERE id = ?", id) or []
        country_code: str = rows[0]["country_code"]
        cities = get_cities(country_code)

        return render_template('/search_city_info.html', cities=cities)

@app.route("/show_city_info", methods=["GET"])
@login_required
def show_city_info():
    city = request.args.get("city")
    if not city:
        return 'nice try! dont manually insert city in the url', 400

    rows: list[dict]= SQL("SELECT country_code FROM users WHERE id = ?", session['user_id']) or []
    country_code = rows[0]['country_code'] 

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    query = f"{city},{country_code}"
    unit = "metric"

    url = f"{base_url}?q={query}&appid={API_KEY}&units={unit}"
    response= requests.get(url)
    data: dict = response.json()

    if data.get("cod") != 200:
        flash(f"{data.get("message", "Unknown error")}", "danger")
        return redirect(url_for("search_city_info"))

    weather_info: dict = {
        'status':data['weather'][0]['description'], 
        'temperature' : float(data['main']['temp']),
        'wind' : float(data['wind']['speed'])
    }
    session['weather_info'] = weather_info
    session['last_city'] = city
    return render_template("show_city_info.html", weather_info=weather_info)



@app.route("/add_city_info", methods=["POST"])
@login_required
def add_city_info():
    weather_info: dict = session.get('weather_info', "")

    rows: list[dict] = SQL("SELECT country_code FROM users WHERE id = ?",session['user_id']) or []
    country_code = rows[0]['country_code'].upper()

    SQL(
        "INSERT INTO weather_data(user_id, country_code, city, status, temperature, windspeed) VALUES (?, ?, ?, ?, ?, ?)",
        session['user_id'],
        country_code,
        session['last_city'],
        weather_info['status'],
        weather_info['temperature'],
        weather_info['wind']
    )
    flash('city added', 'success')
    session.pop('weather_info', None)
    return redirect(url_for("index"))
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
