# 📝 Todo App – Flask

Aplicación web para gestión de tareas con autenticación de usuarios, desarrollada con **Flask**, **SQLAlchemy** y **PostgreSQL**.  
Incluye soporte para listas de tareas, prioridades y estados.

---

## 🚀 Funcionalidades

- Registro y login de usuarios (Flask-Login)
- CRUD completo de tareas
- Listas de tareas personalizadas
- Prioridades (baja, media, alta)
- Estado de tarea (hecha / pendiente)
- Protección de rutas mediante decoradores
- Persistencia con SQLAlchemy
- Interfaz web con Bootstrap

---

## 🛠 Tecnologías utilizadas

- Python 3
- Flask
- SQLAlchemy
- PostgreSQL (producción / Docker)
- SQLite (modo local opcional)
- Docker & Docker Compose
- HTML + Bootstrap 5

---

## 📦 Instalación (modo local)

```bash
git clone <repo>
cd todo_app

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

pip install -r requirements.txt
python run.py
