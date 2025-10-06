from flask import current_app, render_template, redirect, url_for, session, flash, request
import requests
from ..util import SQL, login_required, get_country_dict, get_cities
from flask import Blueprint
weather = Blueprint("weather", __name__)




@weather.route("/search_city_info", methods=["GET","POST"])
def search_city_info():
    if request.method == "POST":
        city: str = request.form.get("city", "")
        if not city:
            flash("Enter a valid city name!", "danger")
            return redirect(url_for("weather.search_city_info"))
        return redirect(url_for("weather.show_city_info", city=city))
            
    elif request.method == "GET":       
        id = session['user_id']
        rows: list[dict] = SQL("SELECT country_name FROM users WHERE id = ?", id) or []
        country_name: str = rows[0]["country_name"]
        country_name = get_country_dict()[country_name]
        cities = get_cities(country_name)

        return render_template('weather/search_city_info.html', cities=cities)

@weather.route("/show_city_info", methods=["GET"])
@login_required
def show_city_info():
    city = request.args.get("city")
    if not city:
        return 'nice try! dont manually insert city in the url', 400

    rows: list[dict]= SQL("SELECT country_name FROM users WHERE id = ?", session['user_id']) or []
    country_name = rows[0]['country_name']
    country_code = get_country_dict()[country_name]

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    query = f"{city},{country_code}"
    unit = "metric"
    API_KEY = current_app.config['OPENWEATHER_API_KEY']
    url = f"{base_url}?q={query}&appid={API_KEY}&units={unit}"
    response= requests.get(url)
    data: dict = response.json()

    if data.get("cod") != 200:
        flash(f"{data.get("message", "Unknown error")}", "danger")
        return redirect(url_for("weather.search_city_info"))

    weather_info: dict = {
        'status':data['weather'][0]['description'], 
        'temperature' : float(data['main']['temp']),
        'wind' : float(data['wind']['speed'])
    }
    session['weather_info'] = weather_info
    session['last_city'] = city
    return render_template("weather/show_city_info.html", weather_info=weather_info)



@weather.route("/add_city_info", methods=["POST"])
@login_required
def add_city_info():
    weather_info: dict = session.get('weather_info', "")

    rows: list[dict] = SQL("SELECT country_name FROM users WHERE id = ?",session['user_id']) or []
    country_name = rows[0]['country_name']

    SQL(
        "INSERT INTO weather_data(user_id, country_name, city, status, temperature, windspeed) VALUES (?, ?, ?, ?, ?, ?)",
        session['user_id'],
        country_name,
        session['last_city'],
        weather_info['status'],
        weather_info['temperature'],
        weather_info['wind']
    )
    flash('city added', 'success')
    session.pop('weather_info', None)
    return redirect(url_for("dashboard.index"))
