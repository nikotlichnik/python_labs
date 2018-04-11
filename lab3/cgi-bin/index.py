import sqlite3
import os


# Функция соединения с БД
def connect_db():
    con = sqlite3.connect("ISU.db")
    return con


# Получение списка таблиц в БД
def get_tables_list(con):
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name ASC")
    query_list = cur.fetchall()

    # Распаковка массива кортежей в обычный массив
    tables_list = []
    for table in query_list:
        tables_list.append(table[0])

    # Удаление служебной таблицы
    tables_list.remove("sqlite_sequence")

    cur.close()
    return tables_list


# Получение списка элементов option для формы
def get_option_list(list_of_elements):
    options = ""
    for element in list_of_elements:
        options += "<option value='" + element + "'>" + element + "</option>"
    return options


conn = connect_db()
list_of_tables = get_tables_list(conn)
table_options = get_option_list(list_of_tables)

print("Content-type: text/html")
print("\n")
print("<meta charset='utf-8'><h1>Лабораторная №3 CGI</h1>")

print("<h2>Запись в таблицу</h2>")
print("""<form action='write_to_db.py' method='post'>
            <select name='table'>{0}</select> 
            <button type='submit' name='db_write'>Выбрать</button>   
         </form>""".format(table_options))

print("<h2>Просмотр таблицы</h2>")
print("""<form action='show_from_db.py' method='post'>
            <select name='table'>{0}</select> 
            <button type='submit' name='db_show'>Выбрать</button>   
         </form>""".format(table_options))

print("<p>Автор: Штрейс Никита, гр.P3320</p>")