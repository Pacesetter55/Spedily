import os
import functools
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, get_user_by_email, get_user_by_username, create_user

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
init_db()


# ------------------------------------------------------------------ #
# Auth helpers                                                        #
# ------------------------------------------------------------------ #

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", form={})

    name     = request.form.get("name",     "").strip()
    email    = request.form.get("email",    "").strip()
    password = request.form.get("password", "")
    form     = {"name": name, "email": email}

    if not name or not email or not password:
        return render_template("register.html", error="All fields are required.", form=form)

    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.", form=form)

    if get_user_by_email(email):
        return render_template("register.html", error="An account with that email already exists.", form=form)

    if get_user_by_username(name):
        return render_template("register.html", error="That username is already taken.", form=form)

    create_user(name, email, generate_password_hash(password))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('user_id'):
        return redirect(url_for('profile'))

    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email",    "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="All fields are required.")

    user = get_user_by_email(email)
    if not user or not check_password_hash(user['password_hash'], password):
        return render_template("login.html", error="Invalid email or password.")

    session.clear()
    session['user_id']  = user['id']
    session['username'] = user['username']

    next_url = request.args.get('next')
    return redirect(next_url if next_url else url_for('profile'))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for('landing'))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
