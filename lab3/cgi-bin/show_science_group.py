import cgi
import html
import sqlite3


# Функция соединения с БД
def connect_db():
    con = sqlite3.connect("ISU.db")
    return con


# Получение названия группы
def get_group_name(con, group_id):
    cur = con.cursor()
    cur.execute(
        "SELECT sg.`name` FROM Scientific_groups sg WHERE sg.id = {0}".format(group_id))
    group_name = cur.fetchone()[0]
    cur.close()
    return group_name


# Получение руководителя группы
def get_group_head(con, group_id):
    cur = con.cursor()
    cur.execute(
        "SELECT t.`surname`, t.`name`, t.`middlename` FROM Scientific_groups sg, Teachers t WHERE sg.id = {0} AND sg.head = t.id".format(
            group_id))
    query_list = cur.fetchone()
    group_head = ""
    for part in query_list:
        group_head += part + " "
    cur.close()
    return group_head


# Формирование таблицы из списка студентов в научной группе
def make_students_table(con, group_id):
    cur = con.cursor()
    cur.execute(
        "SELECT s.`surname`, s.`name`, s.`middlename`, g.`number` FROM Scientific_group_Student sgs, Students s, Groups g WHERE sgs.scientific_group_id = {0} AND sgs.student_id = s.id AND s.group_id = g.id ORDER BY s.`surname` ASC".format(
            group_id))
    query_list = cur.fetchall()

    table = """<table border=1>
                    <tr>
                        <th>№ п/п</th>
                        <th>Студент</th>
                        <th>Группа</th>
                    </tr>
            """

    for key, student_info in enumerate(query_list, 1):
        student_group = student_info[3]
        student_name = student_info[0] + " " + student_info[1] + " " + student_info[2]
        table += """<tr>
                        <td>{0}</td>
                        <td>{1}</td>
                        <td>{2}</td>
                    </tr>""".format(key, student_name, student_group)

    table += "</table>"
    cur.close()
    return table


print("Content-type: text/html")
print("\n")
print("<meta charset='utf-8'>")

form = cgi.FieldStorage()

# Выход из программы, если не передан параметр id группы
if "id" not in form.keys():
    print("<h1>Ошибка!</h1>")
    exit(0)

conn = connect_db()

group_id = form["id"].value
group_name = get_group_name(conn, group_id)
group_head = get_group_head(conn, group_id)

print("<h1>Просмотр научной группы</h1>")
print("<h2>Действия</h2>")
print("""<a href='index.py'>На главную</a><br>""")
print("""<a href='add_student_to_science_group.py?id={0}'>Добавить студента в группу</a>""".format(group_id))

print("<h2>Название группы</h2>")
print(group_name)

print("<h2>Руководитель группы</h2>")
print(group_head)

print("<h2>Состав группы</h2>")
print(make_students_table(conn, group_id))
