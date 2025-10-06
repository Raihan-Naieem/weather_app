from flask import render_template, redirect, url_for, request, flash, session
from ..util import SQL, get_country_dict, login_required
from flask import Blueprint
dashboard = Blueprint("dashboard", __name__)




@dashboard.route("/", methods=["GET", "POST"])
@login_required
def index():
    # TODO: 
    # will show added city with pagination and can delete
    # some basic data manipulation (ex highest temp, avg temp etc)

    if request.method == "GET":
        weather_data_set: list[dict] = SQL('''
            SELECT
                id,
                country_name, 
                city,
                status, 
                temperature, 
                windspeed, 
                timestamp 
            FROM weather_data 
            WHERE user_id = ?
            ''', session["user_id"]) or []

        rows: list[dict] = SQL("SELECT country_name FROM users WHERE id = ?", session["user_id"]) or []
        current_country_name: str = rows[0]["country_name"].capitalize()
        


        return render_template("dashboard/index.html", 
                               weather_data_set=weather_data_set, 
                               current_country_name=current_country_name
                               ,available_names=list(get_country_dict().keys()))

@dashboard.route("/update_country_name", methods=["POST"])
def update_country_name():
    update_name = request.form.get("country_name", "").strip().capitalize()
    available_names = list(get_country_dict().keys())

    if not update_name:
        flash("Country name cannot be empty!", "danger")
        return redirect(url_for("dashboard.index"))

    if update_name not in available_names:
        flash("Invalid updated country name!", "danger")
        return redirect(url_for("dashboard.index"))

    SQL('''
        UPDATE users 
        SET country_name = ? 
        WHERE id = ?
        ''', update_name, session["user_id"])
    flash("Country name updated!", "success")
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




