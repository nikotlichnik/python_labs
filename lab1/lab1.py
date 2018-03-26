# Программа преобразования CSV файла списка группы
# ИТМО в XML файл с разделением студентов по полу
#
# Автор - Штрейс Никита, гр.P3320

import csv
from lxml import etree


# Функция разбивки имени на составляющие части
def get_name(fullname):
    name_parts = fullname.split()

    surname = name_parts[0]
    name = name_parts[1]

    # Проверка наличия отчества
    if len(name_parts) == 3:
        middle_name = name_parts[2]
    else:
        middle_name = ""

    return (surname, name, middle_name)


# Открытие CSV файла
file = open('../../group-list2.csv')
reader = csv.reader(file, delimiter=';')

# Проход по строкам CSV файла
for row in reader:

    # Получение номера группы из первой строки
    if reader.line_num == 1:
        group_number = row[0].split()[2]

        # Создание корня XML файла
        root = etree.Element("group", number=group_number)
        # Создание мужской и женской подгрупп
        male_group = etree.SubElement(root, "subgroup", gender='male')
        female_group = etree.SubElement(root, "subgroup", gender='female')
        continue

    # Пропуск второй и третьей строк без данных
    if reader.line_num == 2 or reader.line_num == 3:
        continue

    # Пропуск последних двух строк без данных
    if (row[0] == '') or ("Отчет" in row[0]):
        continue

    # Получение данных о студенте
    id = row[1]
    surname, name, middle_name = get_name(row[2])

    # Проверка пола студента и запись в структуру XML
    if row[3].lower() == 'м':
        male_group.append(etree.Element("student", name=name, surname=surname, middle_name=middle_name, id=id))
    elif row[3].lower() == 'ж':
        female_group.append(etree.Element("student", name=name, surname=surname, middle_name=middle_name, id=id))

# Запись в файл
f = open('../../' + group_number + '.xml', 'w')
f.write('<?xml version="1.0" encoding="windows-1251"?>\n')
f.write(etree.tostring(root, pretty_print=True, encoding="utf-8").decode('utf-8'))
f.close()
