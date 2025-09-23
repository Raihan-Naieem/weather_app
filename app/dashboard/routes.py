from flask import render_template, redirect, url_for, request, flash, session
from ..util import SQL, login_required, get_country_codes
from flask import Blueprint
dashboard = Blueprint("dashboard", __name__)




@dashboard.route("/", methods=["GET", "POST"])
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
            return redirect(url_for('weather.search_city_info'))

        rows: list[dict] = SQL("SELECT country_code FROM users WHERE id = ?", session["user_id"]) or []
        current_country_code = rows[0]["country_code"].upper()


        return render_template("dashboard/index.html", 
                               weather_data_set=weather_data_set, 
                               current_country_code=current_country_code
                               ,available_codes=get_country_codes())

@dashboard.route("/update_country_code", methods=["POST"])
def update_country_code():
    update_code = request.form.get("country_code", "").strip().upper()
    available_codes = get_country_codes()

    if not update_code:
        flash("Country code cannot be empty!", "danger")
        return redirect(url_for("dashboard.index"))

    if update_code not in available_codes:
        flash("Invalid updated country code!", "danger")
        return redirect(url_for("dashboard.index"))

    SQL('''
        UPDATE users 
        SET country_code = ? 
        WHERE id = ?
        ''', update_code, session["user_id"])
    flash("Country code updated!", "success")
    return redirect(url_for("dashboard.index"))

@dashboard.route("/delete_row", methods=["POST"])
def delete_row():
    id = request.args.get('id', type=int)
    if not id:
        flash("Deletion error!")
        return redirect(url_for("dashboard.index"))
    SQL('''
        DELETE FROM weather_data 
        WHERE id = ? AND 
        user_id = ?
        ''', id, session["user_id"])
    return redirect(url_for("dashboard.index"))




