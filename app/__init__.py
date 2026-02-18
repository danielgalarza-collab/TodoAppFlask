from flask import Flask
from .routes.auth import auth_bp
from .routes.tasks import tasks_bp
from .extensions import db

def create_app(template_folder=None):
    app = Flask(__name__, template_folder="../templates")
    app.config['SECRET_KEY'] = 'tu_clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app

