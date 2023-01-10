import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request


status = [
    {'new': ""},
    {'pending': 'модератор взял в работу'},
    {'accepted': 'модерация прошла успешно'},
    {'rejected': 'модерация прошла, информация не принята'}
]


level = [
    {"winter": ""},
    {"summer": "1А"},
    {"autumn": "1А"},
    {"spring": ""}
]


state = [
    {'1': 'успешно удалось отредактировать запись в базе данных'},
    {'0': 'обновить запись не удалось: редактировать можно все поля,\
     (кроме ФИО, адрес почты и номер телефона)'}
]


CREATE_USER_TABLE = (
    "CREATE TABLE IF NOT EXIST user (full_name CHAR(255) NOT NULL,\
    phone INT(11) NOT NULL, CONSTRAINT email UNIQUE (user_id), FOREIGN KEY (id_pereval_added);"
)


CREATE_TABLE_PEREVAL_ADDED = (
    "CREATE TABLE IF NOT EXIST pereval_added (id PRIMARY KEY, beautyTitle CHAR(255) NOT NULL,\
     title CHAR(255) NOT NULL, other_titles CHAR(255) NOT NULL, connect CHAR(255), add_time DATETIME NOT NULL,\
     level TEXT, status DEFAULT, FOREIGN KEY(coord_id));"
)


CREATE_TABLE_COORDS = (
    "CREATE TABLE IF NOT EXIST coords(latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, height INT NOT NULL,\
    PRIMARY KEY (coord_id), FOREIGN KEY (id_pereval_added);"
)


CREATE_TABLE_IMAGES = (
    "CREATE TABLE IF NOT EXIST pereval_images(images_id PRIMARY KEY NOT NULL, FOREIGN KEY (id_pereval_added);"
)


ADD_STATUS = (
    "ALTER TABLE pereval_added ADD COLUMN IF NOT EXISTS status DEFAULT new;"
)


load_dotenv()


app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.post("/api/pereval_added")
def pereval_added():
    data = request.get_json()
    pereval_added = data["pereval_added"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE_PEREVAL_ADDED)
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(CREATE_TABLE_COORDS)
            cursor.execute(CREATE_TABLE_IMAGES)
    return pereval_added


@app.post("/api/submitData")
def submitData():
    data = request.get_json()
    status = data["status"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ADD_STATUS, (status,))
    return {'message': f'{status}'}


@app.get("/api/submitData/<id>")
def id_pereval():
    connection = psycopg2.connect("DATABASE_URL")
    with connection:
        with connection.cursor() as cursor:
            cursor(f'SELECT * FROM pereval_added')
    return pereval_added.query.all()


@app.patch("/api/submitData/<id>")
def update_pereval():
    data = request.get_json()
    if status is 'new':
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_TABLE_PEREVAL_ADDED)
        return {'message': f'{state}'}, 1
    else:
        return {'message': f'{state}'}, 0


@app.get("/api/?user__email=<email>")
def email_id_add_pereval():
    connection = psycopg2.connect("DATABASE_URL")
    with connection:
        with connection.cursor() as cursor:
            cursor(f'SELECT * FROM pereval_added ORDER BY email_id')
        return cursor.fetchall()


