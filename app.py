
from typing import Any
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


@app.route("/", methods=["GET"])
@login_required
def index():
    return redirect(url_for("search_city"))


@app.route("/search_city", methods=["GET","POST"])
def search_city():
    if request.method == "POST":
        city: str | None = request.form.get("city")
        if city:
            return redirect(url_for("show_city_info", city=city))
        else: #TODO: change later 
            return 'Please enter a city name', 400
            
    else:
        
        id = session['user_id']
        rows: list[dict] = SQL("SELECT country_code FROM users WHERE id = ?", id) or []
        country_code: str = rows[0]["country_code"]
        cities: list[str] = get_cities(country_code)

        return render_template('/search_city.html', cities=cities)

@app.route("/show_city_info", methods=["GET", "POST"])
@login_required
def show_city_info():
    if request.method == 'POST':
        id = session['user_id']
        city = request.form.get("city")
        if not city:
            return 'error', 400

        rows: list[dict]= SQL("SELECT country_code FROM users WHERE id = ?", id)
        country_code = rows[0]['country_code'] 

        base_url = "https://api.openweathermap.org/data/2.5/weather"
        query = f"{city},{country_code}"
        unit = "metric"

        url = f"{base_url}?q={query}&appid={API_KEY}&units={unit}"
        response= requests.get(url)
        data: dict = response.json()
        weather_info = {'status':data['weather'][0]['description'], 'temperature' : data['main']['temp'], 'wind' : data['wind']['speed']} 
        return render_template("show_city_info.html", weather_info=weather_info)
    else:
        return render_template(url_for('show_city_info'))



# AUTH
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        country_code = request.form.get("country_code")
        country_codes: list[str] = get_country_codes()

        if country_code not in country_codes:
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
    
    else:
        # to give user a drop down box of country codes to select from
        country_codes = get_country_codes()
        return render_template("register.html", navbar=False, country_codes= country_codes)

@app.route("/login", methods=['GET', 'POST'])
def login():

    # session.clear()
    
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
    else:
        return render_template("login.html",navbar=False)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))






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
    app.run(host='0.0.0.0', debug=True)
