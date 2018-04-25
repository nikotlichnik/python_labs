import cgi
import sqlite3
import os


# Функция соединения с БД
def connect_db():
    con = sqlite3.connect("ISU.db")
    return con


# Получение списка возможных руководителей научных групп
def get_heads_list(con):
    cur = con.cursor()
    cur.execute("SELECT t.id, t.`surname`, t.`name`, t.`middlename` FROM Teachers t ORDER BY t.`surname` ASC")
    heads_list = cur.fetchall()
    cur.close()
    return heads_list


# Получение списка элементов option для формы
def get_option_list(list_of_elements):
    options = ""
    for element in list_of_elements:
        options += "<option value='{0}'>{1} {2} {3}</option>".format(element[0], element[1], element[2], element[3])
    return options

conn = connect_db()
list_of_heads = get_heads_list(conn)
heads_options = get_option_list(list_of_heads)

print("Content-type: text/html")
print("\n")
print("<meta charset='utf-8'><h1>Добавление новой научной группы</h1>")


# Проверка отправки формы
form = cgi.FieldStorage()
if "group_name" in form.keys():
    cur = conn.cursor()
    cur.execute("INSERT INTO Scientific_groups (name, head) VALUES (?, ?)",
                (form['group_name'].value, form['group_head'].value))
    print("Добавлена новая группа.")
    conn.commit()
    cur.close()

print("<h2>Действия</h2>")
print("""<a href='index.py'>На главную</a>""")

print("<h2>Создать новую научную группу</h2>")
print("""<form action='add_science_group.py' method='post'>
            Название <input type='text' name='group_name'>
            Руководитель <select name='group_head'>{0}</select> 
            <button type='submit' name='add_group'>Создать</button>   
         </form>""".format(heads_options))
