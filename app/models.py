from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from app.extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, unique=True)
    password_hash = db.Column(db.Text, nullable=False)

    tasks = db.relationship("Task", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    done = db.Column(db.Boolean, default=False)

    parent_task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id", ondelete="CASCADE")
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    list_id = db.Column(
        db.Integer,
        db.ForeignKey("lists.id", ondelete="SET NULL")
    )
    list = db.relationship("List", back_populates="tasks")

    priority_id = db.Column(
        db.Integer,
        db.ForeignKey("priorities.id")
    )

    status_id = db.Column(
        db.Integer,
        db.ForeignKey("statuses.id")
    )

    #Relaciones ORM
    user = db.relationship("User", back_populates="tasks")
    status = db.relationship("Status")
    priority = db.relationship("Priority")
    parent_task = db.relationship("Task", remote_side=[id])



class Status(db.Model):
    __tablename__ = "statuses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        return f"<Status {self.name}>"

class Priority(db.Model):
    __tablename__ = "priorities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class List(db.Model):
    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    tasks = db.relationship("Task", back_populates="list")
