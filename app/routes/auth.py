from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import db
from app.models import User, Status, Priority, Task
from sqlalchemy import text
from flask_login import login_user, logout_user, login_required, current_user


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

    login_user(user) 

    return redirect(url_for("tasks.index"))


#@auth_bp.route("/logout")
#def logout():
   # session.pop("user_id", None)
   # return redirect(url_for("auth.login"))



@auth_bp.route("/test_db")
def test_db():
    try:
        db.session.execute(text("SELECT 1"))
        return "Conexión a PostgreSQL OK"
    except Exception as e:
        return f"error: {e}"

@auth_bp.route("/test_status")
def test_status():
    statuses = Status.query.all()
    return ", ".join([s.name for s in statuses])

@auth_bp.route("/test_priorities")
def test_priorities():
    priorities = Priority.query.all()
    return ", ".join([p.name for p in priorities])


@auth_bp.route("/test_tasks")
@login_required
def test_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return str(tasks)

@auth_bp.route("/create_test_task")
def create_test_task():
    user = User.query.first()
    status = Status.query.first()
    priority = Priority.query.first()

    if not user or not status or not priority:
        return "Faltan datos en la base (user/status/priority)"

    task = Task(
        title="Primera tarea real",
        description="Probando relaciones ORM",
        user_id=user.id,
        status_id=status.id,
        priority_id=priority.id
    )

    db.session.add(task)
    db.session.commit()

    return "Tarea creada correctamentee"

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logout exitoso"
