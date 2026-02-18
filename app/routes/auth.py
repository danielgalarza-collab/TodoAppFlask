from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not email or not password:
        flash("Todos los campos son obligatorios")
        return redirect(url_for("auth.register"))

    if User.query.filter_by(username=username).first():
        flash("El usuario ya existe")
        return redirect(url_for("auth.register"))

    if User.query.filter_by(email=email).first():
        flash("El email ya está registrado")
        return redirect(url_for("auth.register"))

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id
    return redirect(url_for("tasks.index"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    identifier = request.form.get("identifier")
    password = request.form.get("password")

    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if user is None or not user.check_password(password):
        flash("Usuario o contraseña incorrectos")
        return redirect(url_for("auth.login"))

    session["user_id"] = user.id
    return redirect(url_for("tasks.index"))


@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))
