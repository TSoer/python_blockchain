"""
Все достаточно просто в данном скрипте представлен простейшая реализация гениальной технологии blockchain,
конец одного блока является частью следующего блока это позволяет отлавливать изменения в цепи
скрипт представлен тремя основными функциями:
1. get_hash предназначена для получения hash блока
2. write_block призванная записать следующий блок в папку blockchain
3. check_integrity проходит по всем блокам цепи и возвращает ответ о состоянии блоков (изменен ли блок или нет)

В данном скрипте реализована простейшая система записи учета кредитов "займов" от одного лица к другому
подробнее: https://www.youtube.com/watch?v=JxPWs8Ojdx8
"""

import os
import json
import hashlib

# Задаем отсновну директорию
blockchain_dir = os.curdir + '/blockchain/'


def get_files():
    """
    Функция получает полный список блоков и сортирует его
    :return: list
    """
    files = os.listdir(blockchain_dir)
    return sorted([int(i) for i in files])


def get_hash(filename):
    """
    Функция получает имя фала получает md5 hash и  возращает hash блока
    :param filename: имя файла
    :return: hash block
    """
    global blockchain_dir
    file = open(blockchain_dir + filename, 'rb').read()
    return hashlib.md5(file).hexdigest()


def check_integrity():
    """
    Данная функции проходится по всей цепочки blockchain и определяет какой блок был изминен
    :return: Возрашает список с результами
    """
    # Создаем список в который будет записываться результаты проверки
    result = []

    files = get_files()
    for file in files[1:]:
        h = json.load(open(blockchain_dir + str(file)))['hash']
        # Вычисляем hash блока предыдкщего блока чтобы в дальнейшим сравнить
        prev_file = str(file - 1)
        actual_hash = get_hash(prev_file)

        # Задаем условия выбора
        if h == actual_hash:
            res = 'Ok'
        else:
            res = 'Corrupted'
        result.append({'block': prev_file, 'result': res})

    return result


def write_block(name, amount, to_whoe, prev_hash=''):
    """
    Функция записывает данный в блок
    :param name: имя кредитора
    :param amount: имя заемщика
    :param to_whoe: объем занимаемых средств
    :param prev_hash: hash прошлого блока по умолчанию None
    :return: записывает следующий блок
    """

    # Находим номер последнего блока
    files = get_files()
    last_file = files[-1]
    filename = str(last_file + 1)

    # Вычесляем hash последнего блока в цепи
    prev_hash = get_hash(str(last_file))

    # Определяю фориат блока
    data = {'name': name,
            'amount': amount,
            'to_whoe': to_whoe,
            'hash': prev_hash}

    # Записываем следующи блок в директорию
    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    # Сдесь вызываем фукцию записи и передаем ей данные которые хотели бы записать в следующий блок
    write_block(name='oleg', amount=50, to_whoe='oksana')
    result = check_integrity()
    print(result)


if __name__ == '__main__':
    main()