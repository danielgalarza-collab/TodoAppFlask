from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="todo_app",
        user="daniel",
        password="daniel"
    )
    return conn
