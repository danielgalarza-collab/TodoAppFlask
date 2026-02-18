from flask import Blueprint, render_template, request, redirect, url_for, session
from app.extensions import db
from app.models import Task
from app.decorators import login_required

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/")
@login_required
def index():
    tareas = Task.query.filter_by(user_id=session["user_id"]).all()
    return render_template("index.html", tareas=tareas)


@tasks_bp.route("/add", methods=["POST"])
@login_required
def add():
    nueva_tarea = Task(
        title=request.form["title"],
        description=request.form["description"],
        priority=request.form["priority"],
        user_id=session["user_id"]
    )

    db.session.add(nueva_tarea)
    db.session.commit()

    return redirect(url_for("tasks.index"))


@tasks_bp.route("/completar/<int:id>", methods=["POST"])
@login_required
def completar(id):
    tarea = Task.query.get_or_404(id)

    if tarea.user_id != session["user_id"]:
        return redirect(url_for("tasks.index"))

    tarea.done = not tarea.done
    db.session.commit()

    return redirect(url_for("tasks.index"))


@tasks_bp.route("/editar/<int:id>", methods=["POST"])
@login_required
def editar(id):
    tarea = Task.query.get_or_404(id)

    if tarea.user_id != session["user_id"]:
        return redirect(url_for("tasks.index"))

    tarea.title = request.form["nuevo_titulo"]
    tarea.description = request.form["nueva_descripcion"]

    db.session.commit()

    return redirect(url_for("tasks.index"))


@tasks_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    tarea = Task.query.get_or_404(id)

    if tarea.user_id != session["user_id"]:
        return redirect(url_for("tasks.index"))

    db.session.delete(tarea)
    db.session.commit()

    return redirect(url_for("tasks.index"))
