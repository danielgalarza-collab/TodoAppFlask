from flask import Flask
from .routes.auth import auth_bp
from .routes.tasks import tasks_bp
from .extensions import db
from app.models import User
from flask_login import LoginManager

login_manager = LoginManager()

def create_app(template_folder=None):
    app = Flask(__name__, template_folder="../templates")

    app.config['SECRET_KEY'] = 'tu_clave_secreta'
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://daniel:daniel@localhost/todo_app"
   # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    @app.route("/")
    def home():
        return "Servidor funcionando"
    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
