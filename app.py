import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request


STATUS = [
    {'new': ""},
    {'pending': 'модератор взял в работу'},
    {'accepted': 'модерация прошла успешно'},
    {'rejected': 'модерация прошла, информация не принята'}
]

LEVEL = [
    {"winter": ""},
    {"summer": "1А"},
    {"autumn": "1А"},
    {"spring": ""}
]


CREATE_USER_TABLER = (
    "CREATE TABLE IF NOT EXIST user (id SERIAL PRIMARY KEY, full_name CHAR(255) NOT NULL,\
    phone INT(11) NOT NULL, CONSTRAINT email UNIQUE (user_id), FOREIGN KEY(coord_id);"
)


CREATE_TABLE_PEREVAL_ADDED = (
    "CREATE TABLE IF NOT EXIST pereval_added (id SERIAL PRIMARY KEY, beautyTitle CHAR(255) NOT NULL,\
     title CHAR(255) NOT NULL, other_titles CHAR(255) NOT NUL, connect CHAR(255), add_time DATETIME NOT NULL,\
     level LEVEL);"
)


CREATE_TABLE_COORDS = (
    "CREATE TABLE IF NOT EXIST coords(latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, height INT NOT NULL,\
    PRIMARY KEY (coord_id);"
)


CREATE_TABLE_IMAGES = (
    "CREATE TABLE IF NOT EXIST pereval_images(images_id PRIMARY KEY NOT NULL, FOREIGN KEY (id_pereval_added);"
)

ADD_STATUS = ("ALTER TABLE pereval_added ADD COLUMN IF NOT EXISTS status STATUS;")


load_dotenv()


app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/api/pereval_added")
def submitData():
    data = request.get_json()
    status = data["status"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ADD_STATUS)
    return f'Статус{status}'