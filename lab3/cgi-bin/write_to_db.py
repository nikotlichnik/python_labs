import cgi
import html
import sqlite3

# Функция соединения с БД
def connect_db():
    con = sqlite3.connect("ISU.db")
    return con

# Получение списка полей в таблице
def get_columns(con, table):
    # TODO Получение списка полей для вставки данных в любую таблицу
    sql = "pragma table_info({0})".format(table)
    return


print("Content-type: text/html")
print("\n")
print("<meta charset='utf-8'>")

form = cgi.FieldStorage()

# Выход из программы, если не передан параметр
if "table" not in form.keys():
    print("<h1>Ошибка!</h1>")
    exit(0)

# Получаем название таблицы
table_name = form["table"].value
conn = connect_db()



print("<h1>Запись данных в таблицу \"" + table_name + "\"</h1>")
print("<p>Форма</p>", form.keys())
