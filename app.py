from flask import Flask, request, jsonify, g
from flask_cors import CORS
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Crie um pool de conexões para o banco de dados
db_url = os.environ.get("DATABASE_URL")
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20, db_url)

# Tabela de criação e inserção
CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, address TEXT, phone TEXT, email TEXT)"
)
INSERT_USER = "INSERT INTO users (name, address, phone, email) VALUES (%s, %s, %s, %s) RETURNING id"
GET_USERS = "SELECT * FROM users"
CREATE_SUBJECT_TABLE = (
    "CREATE TABLE IF NOT EXISTS subjects (id SERIAL PRIMARY KEY, user_id INTEGER, title TEXT, description TEXT, date TEXT, resolved BOOLEAN, FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE)"
)
INSERT_SUBJECT = "INSERT INTO subjects (user_id, title, description, date, resolved) VALUES (%s, %s, %s, %s, %s)"
RESOLVE_SUBJECT = "UPDATE subjects SET resolved = %s WHERE id = %s"
GET_SUBJECT_BY_ID = "SELECT * FROM subjects WHERE id = %s"
GET_SUBJECTS = "SELECT * FROM subjects"
GET_USER_NAME_BY_Id = "SELECT name FROM users WHERE id = %s"
GET_USER_ID_BY_EMAIL = "SELECT id FROM users WHERE email = %s"

# Função para abrir a conexão de banco de dados por requisição
def get_db_conn():
    if 'db_conn' not in g:
        g.db_conn = connection_pool.getconn()
    return g.db_conn

# Função para fechar a conexão de banco de dados após a requisição
@app.teardown_appcontext
def close_db_conn(exception):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        connection_pool.putconn(db_conn)

@app.post("/api/users")
def create_user():
    data = request.get_json()
    name = data["name"]
    address = data["address"]
    phone = data["phone"]
    email = data["email"]
    
    db_conn = get_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(CREATE_USERS_TABLE)
        cursor.execute(INSERT_USER, (name, address, phone, email))
        user_id = cursor.fetchone()[0]
        db_conn.commit()
    
    return {"message": f"Usuário {name} com Id {user_id} criado com sucesso."}, 201

@app.get("/api/users")
def get_users():
    db_conn = get_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(GET_USERS)
        users = cursor.fetchall()
    return jsonify(users)

@app.post("/api/subject")
def create_subject():
    data = request.get_json()
    user_email = data["user_email"]
    title = data["title"]
    description = data["description"]
    resolved = data["resolved"]
    date = data["date"]

    print(data)
    print(user_email)

    db_conn = get_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(GET_USER_ID_BY_EMAIL, (user_email,))
        user_id = cursor.fetchone()[0]
        cursor.execute(CREATE_SUBJECT_TABLE)
        cursor.execute(INSERT_SUBJECT, (user_id, title, description, date, resolved))
        db_conn.commit()

    return {"message": f"Assunto {title} criado com sucesso."}, 201

@app.get("/api/subjects")
def get_subjects():
    db_conn = get_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(GET_SUBJECTS)
        subjects = cursor.fetchall()
    return jsonify(subjects)

@app.put("/api/resolve-subject")
def resolve_subject():
    data = request.get_json()
    subject_id = str(data["subject_id"])
    resolve = data["resolve"]

    db_conn = get_db_conn()
    with db_conn.cursor() as cursor:
        cursor.execute(GET_SUBJECT_BY_ID, (subject_id,))
        subject = cursor.fetchone()
        if subject is None:
            return {"message": f"Assunto com id {subject_id} não existe"}, 404

        cursor.execute(RESOLVE_SUBJECT, (resolve, subject_id))
        db_conn.commit()
    
    return {"message": f"Assunto com id {subject_id} atualizado com sucesso"}, 200

