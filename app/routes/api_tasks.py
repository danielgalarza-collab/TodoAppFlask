from flask import Blueprint, jsonify, request
from app.models import Task
from flask_login import login_required, current_user
from app.extensions import db

api_tasks_bp = Blueprint("api_tasks", __name__, url_prefix="/api")

@api_tasks_bp.route("/tasks")
@login_required
def get_tasks():

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    #tasks=Task.query.all()
    result = []

    for task in tasks:
        result.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority.name if task.priority else None,
            "status": task.status.name if task.status else None
        })

    return jsonify(result)

from flask import request

@api_tasks_bp.route("/tasks", methods=["POST"])
@login_required
def create_task():

    data = request.get_json()

    new_task = Task(
        title=data["title"],
        description=data.get("description"),
        user_id=current_user.id
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task creada"})

@api_tasks_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task eliminada"
    })

@api_tasks_bp.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):

    task = Task.query.get_or_404(id)

    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)

    db.session.commit()

    return jsonify({
        "message": "Task actualizada"
    })
