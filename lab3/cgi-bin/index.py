import sqlite3
import os


# Функция соединения с БД
def connect_db():
    con = sqlite3.connect("ISU.db")
    return con


# Получение списка научных групп из БД
def get_science_groups(con):
    cur = con.cursor()
    cur.execute(
        "SELECT sg.`name`, t.`surname`, t.`name`, t.`middlename`, sg.`id` FROM Scientific_groups sg, Teachers t WHERE sg.head = t.id ORDER BY sg.`name` ASC")
    query_list = cur.fetchall()

    # Распаковка массива кортежей в обычный массив
    groups_list = []
    for science_group in query_list:
        groups_list.append(science_group)

    cur.close()
    return groups_list


# Формирование таблицы из списка научных групп
def make_science_groups_table(groups_list):
    table = """<table border=1>
                    <tr>
                        <th>№ п/п</th>
                        <th>Название научной группы</th>
                        <th>Руководитель</th>
                    </tr>
            """

    for key, science_group in enumerate(groups_list, 1):
        group_name = science_group[0]
        head_name = science_group[1] + " " + science_group[2][0].upper() + "." + science_group[3][0].upper() + "."
        group_id = science_group[4]
        table += """<tr>
                        <td>{0}</td>
                        <td><a href='show_science_group.py?id={3}'>{1}</a></td>
                        <td>{2}</td>
                    </tr>""".format(key, group_name, head_name, group_id)

    table += "</table>"
    return table


conn = connect_db()
list_of_science_groups = get_science_groups(conn)

print("Content-type: text/html")
print("\n")
print("<meta charset='utf-8'><h1>Лабораторная №3 CGI</h1>")

print("<h2>Действия</h2>")
print("""<a href='add_science_group.py'>Добавить научную группу</a>""")

print("<h2>Список научных групп</h2>")
print(make_science_groups_table(list_of_science_groups))

print("<p>Автор: Штрейс Никита, гр.P3320</p>")
