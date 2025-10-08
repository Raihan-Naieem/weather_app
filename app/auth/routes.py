from typing import Any
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..util import SQL,  get_country_dict, login_required
from flask import Blueprint
auth = Blueprint("auth", __name__)



@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password")
        country_name = request.form.get("country_name")
        country_names: list[str] = list(get_country_dict().keys())


        rows: list[dict[Any, Any]] = SQL("SELECT * FROM users WHERE email = ?", email) or []

        # if user data in database
        if len(rows) != 0:
            flash("email already registered!", "danger")
            return render_template("auth/register.html", navbar=False)

        if not country_name:
            flash("Enter country name!", "danger")
            return render_template("auth/register.html", navbar=False, country_name=country_name)

        country_name = country_name.title()

        if country_name not in country_names:
            flash("Invalid country name!", "danger")
            return render_template("auth/register.html", navbar=False, country_name=country_name)

        if password != confirm_password:
            flash("Password Mismatch", "danger")
            return render_template("auth/register.html", navbar=False, country_name=country_name)

        password_hash = generate_password_hash(password)

        # error if sql isnt working
        try:
            SQL(
                "INSERT INTO users (email, password_hash, country_name) VALUES (?, ?, ?)",
                email,
                password_hash,
                country_name,
            )
        except ValueError as error:
            flash(str(error), "danger")
            return redirect(url_for("auth.register"))

        # Returns a list of one dict where email is matched
        rows: list[dict[Any, Any]] = SQL("SELECT * FROM users WHERE email = ? ", email) or []

        # Remember user id session
        session["user_id"] = rows[0]["id"]

        flash("Registered successfully!", "success")
        return redirect(url_for("auth.login"))

    elif request.method == "GET": 
        # to give user a drop down box of country names to select from
        country_names = list(get_country_dict().keys())
        return render_template("auth/register.html", navbar=False, country_names=country_names)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        rows: list[dict[Any, Any]] = SQL("SELECT * FROM users WHERE email = ?", email) or []

        # if no user data in database
        if len(rows) != 1:
            flash("email not found!", "danger")
            return render_template("auth/login.html", navbar=False)

        password_hash_from_db: str = rows[0]["password_hash"]
        is_password_valid = check_password_hash(password_hash_from_db, password or "")

        if not is_password_valid:
            flash("Invalid Password!", "danger")
            return render_template("auth/login.html", navbar=False)

        # to remember user
        session["user_id"] = rows[0]["id"]
        flash("Logged in succesefully!", "success")
        return redirect(url_for("dashboard.index"))
    elif request.method == "GET":
        return render_template("auth/login.html", navbar=False)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():

    session.clear()
    flash("Logged out!", "danger")
    return redirect(url_for("auth.login"))
