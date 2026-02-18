# migrate_task.py
import json
from datetime import datetime
from app import app
from extensions import db
from models import Task, User

# ID del usuario por defecto al que asignaremos las tareas
DEFAULT_USER_ID = 1

def migrate():
    with app.app_context():
        # Abrimos el JSON con las tareas antiguas
        with open("Borradores/data/task.json", "r") as f:
            tareas_json = json.load(f)

        for tarea in tareas_json:
            # Creamos el objeto Task usando los campos que tienes en tu modelo
            nueva_tarea = Task(
                title=tarea.get("titulo", "Sin título"),
                description=tarea.get("descripcion", ""),
                priority=tarea.get("prioridad", "media"),
                done=tarea.get("completada", False),
                created_at=datetime.strptime(tarea.get("fecha"), "%Y-%m-%d %H:%M:%S"),
                user_id=DEFAULT_USER_ID  # asignamos el usuario por defecto
            )

            db.session.add(nueva_tarea)  # agregamos la tarea a la sesión

        # Guardamos todos los cambios en la base de datos
        db.session.commit()
        print(f"{len(tareas_json)} tareas migradas correctamente!")

if __name__ == "__main__":
    migrate()


