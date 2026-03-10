from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import Task, Priority, List
from flask_login import login_required, current_user

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/")
@login_required
def index():
    tareas = Task.query.filter_by(user_id=current_user.id).all()
    listas = List.query.all()
    return render_template("index.html", tareas=tareas, listas=listas)

@tasks_bp.route("/add", methods=["POST"])
@login_required
def add():

    prioridad_nombre = request.form["priority"]

    prioridad = Priority.query.filter_by(name=prioridad_nombre).first()

    lista_id = request.form.get("list_id")

    nueva_tarea = Task(
        title=request.form["title"],
        description=request.form["description"],
        priority=prioridad,
        user_id=current_user.id,
	list_id=lista_id
    )

    db.session.add(nueva_tarea)
    db.session.commit()

    return redirect(url_for("tasks.index"))


@tasks_bp.route("/completar/<int:id>", methods=["POST"])
@login_required
def completar(id):
    tarea = Task.query.get_or_404(id)

    if tarea.user_id != current_user.id:
        return redirect(url_for("tasks.index"))

    tarea.done = not tarea.done
    db.session.commit()

    return redirect(url_for("tasks.index"))


@tasks_bp.route("/editar/<int:id>", methods=["POST"])
@login_required
def editar(id):
    tarea = Task.query.get_or_404(id)

    if tarea.user_id != current_user.id:
        return redirect(url_for("tasks.index"))

    tarea.title = request.form["nuevo_titulo"]
    tarea.description = request.form["nueva_descripcion"]

    db.session.commit()

    return redirect(url_for("tasks.index"))


@tasks_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    tarea = Task.query.get_or_404(id)

    if tarea.user_id != current_user.id:
        return redirect(url_for("tasks.index"))

    db.session.delete(tarea)
    db.session.commit()

    return redirect(url_for("tasks.index"))

@tasks_bp.route("/add_list", methods=["POST"])
@login_required
def add_list():
    nombre = request.form["name"]
    nueva_lista = List(name=nombre)
    db.session.add(nueva_lista)
    db.session.commit()
    return redirect(url_for("tasks.index"))
