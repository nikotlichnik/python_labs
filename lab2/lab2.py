# coding=UTF-8

# Программа создания базы данных sqlite со
# структурой взаимоотношений в университете
#
# Автор - Штрейс Никита, гр.P3320


import sqlite3
import json
import os


# Функция соединения с БД
def connect_db():
    con = sqlite3.connect("ISU.db")
    return con


# Функция создания БД
def create_db(conn):
    cur = conn.cursor()

    sql = """
    CREATE TABLE Positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL);

    CREATE TABLE Degrees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL);

    CREATE TABLE Interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL);

    CREATE TABLE Teachers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    middlename TEXT,
    gender	TEXT NOT NULL,
    position_id INTEGER REFERENCES Positions(id),	
    degree_id INTEGER REFERENCES Degrees(id));

    CREATE TABLE Teacher_Interest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER REFERENCES Teachers(id),
    interest_id INTEGER REFERENCES Interests(id));

    CREATE TABLE Scientific_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    head INTEGER REFERENCES Teachers(id));

    CREATE TABLE Study_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    name TEXT NOT NULL);

    CREATE TABLE Groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    study_plan_id INTEGER REFERENCES Study_plans(id));

    CREATE TABLE Students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    middlename TEXT,
    gender TEXT NOT NULL,
    group_id INTEGER REFERENCES Groups(id));

    CREATE TABLE Scientific_group_Student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scientific_group_id INTEGER REFERENCES Scientific_groups(id),
    student_id INTEGER REFERENCES Students(id));
    """
    cur.executescript(sql)
    cur.close()


# Функция вставки данных в БД
def insertData(conn, data):
    cur = conn.cursor()

    # Учебные планы
    cur.execute(
        "INSERT INTO Study_plans (id, number, name) VALUES (1, '09.03.02', 'Автоматизация и управление в образовательных системах')")

    # Учебные группы
    cur.execute("INSERT INTO Groups (id, number, study_plan_id) VALUES (1, 'P3320', 1)")

    # Студенты
    for student in data['Students']:
        values = (student['isu_id'], student['name'], student['surname'], student['middlename'], student['gender'], 1)
        cur.execute("INSERT INTO Students (id, name, surname, middlename, gender, group_id) VALUES (?, ?, ?, ?, ?, ?)",
                    values)

    # Должности
    cur.execute("INSERT INTO Positions (id, name) VALUES (1, 'доцент')")
    cur.execute("INSERT INTO Positions (id, name) VALUES (2, 'заведующий кафедрой')")

    # Звания
    cur.execute("INSERT INTO Degrees (id, name) VALUES (1, 'кандидат технических наук')")
    cur.execute("INSERT INTO Degrees (id, name) VALUES (2, 'доктор технических наук')")
    cur.execute("INSERT INTO Degrees (id, name) VALUES (3, 'кандидат педагогических наук')")

    # Преподаватели
    for teacher in data['Teachers']:
        position = teacher['position']
        cur.execute("SELECT id FROM Positions WHERE name = '" + position + "'")
        position_id = cur.fetchone()[0]

        degree = teacher['degree']
        cur.execute("SELECT id FROM Degrees WHERE name = '" + degree + "'")
        degree_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO Teachers (id, surname, name, middlename, gender, position_id, degree_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (teacher['isu_id'], teacher['surname'], teacher['name'], teacher['middlename'], teacher['gender'],
             position_id, degree_id))

    # Интересы
    for interest in data['Interests']:
        try:
            cur.execute("INSERT INTO Interests (name) VALUES ('" + interest + "')")
        except sqlite3.DatabaseError as error:
            pass

    # Связи преподавателей с интересами
    for teacher in data['Teachers']:
        interests = teacher['interests']
        for interest in interests:
            cur.execute("SELECT id FROM Interests WHERE name = '" + interest + "'")
            interest_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Teacher_Interest (teacher_id, interest_id) VALUES (?, ?)",
                        (teacher['isu_id'], interest_id))

    # TODO Создание научных групп

    conn.commit()
    cur.close()


# Удаление существующего файла БД
try:
    os.remove("ISU.db")
except FileNotFoundError:
    pass

# Создание новой БД
con = connect_db()
create_db(con)

# Открытие JSON файла с данными для записи в БД
with open("data/Data.json", encoding="UTF-8") as f:
    isu_data = json.load(f)

# Запись данных в БД
insertData(con, isu_data)

# Закрытие соединения с БД
con.close()
