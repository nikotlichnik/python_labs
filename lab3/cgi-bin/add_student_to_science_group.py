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


# Получение списка возможных студентов для включения в научную группу
def get_students_list(con, group_id):
    cur = con.cursor()
    cur.execute(
        "SELECT s.`id`, s.`surname`, s.`name`, s.`middlename`, g.`number` FROM Students s, Groups g WHERE s.group_id = g.id AND s.id NOT IN (SELECT sgs.student_id FROM Scientific_group_Student sgs WHERE sgs.scientific_group_id = {0}) ORDER BY s.`surname` ASC".format(
            group_id))
    students_list = cur.fetchall()
    cur.close()
    return students_list


# Получение списка элементов option для формы
def get_option_list(list_of_elements):
    options = ""
    for element in list_of_elements:
        options += "<option value='{0}'>{1} {2} {3} - {4}</option>".format(element[0], element[1], element[2],
                                                                           element[3], element[4])
    return options


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

print("<h1>Добавление студента в научную группу</h1>")

# Проверка отправки формы
if "student_id" in form.keys():
    cur = conn.cursor()
    cur.execute("INSERT INTO Scientific_group_Student (scientific_group_id, student_id) VALUES (?, ?)",
                (group_id, form['student_id'].value))
    print("Добавлен новый студент.")
    conn.commit()
    cur.close()

list_of_students = get_students_list(conn, group_id)
student_options = get_option_list(list_of_students)

print("<h2>Действия</h2>")
print("""<a href='index.py'>На главную</a><br>""")
print("""<a href='show_science_group.py?id={0}'>Назад к группе</a>""".format(group_id))

print("<h2>Название группы</h2>")
print(group_name)

print("<h2>Добавить студента</h2>")
print("""<form action='add_student_to_science_group.py?id={1}' method='post'>
            Студент <select name='student_id'>{0}</select> 
            <button type='submit' name='add_student'>Добавить</button>   
         </form>""".format(student_options, group_id))
