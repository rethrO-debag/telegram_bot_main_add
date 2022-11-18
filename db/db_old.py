import sqlite3
from datetime import datetime

conn = sqlite3.connect("Sport.db", check_same_thread=False)
cursor = conn.cursor()

def auth_user(user_id):
    cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
    conn.commit()


def user_exists(user_id):
    """Проверяем, есть ли юзер в базе"""
    print(user_id)
    # Получаем id или None, что соотвествено равно True и False
    result = bool(cursor.execute(f"SELECT `id` FROM `users` WHERE `user_id` = {user_id}").fetchone())
    print('нигер пашет', user_id, result)
    return result


def insert_result(user_id, number_pullups, number_approaches):
    cursor.execute('''INSERT INTO results 
                            ("user_id", "number_pullups", "number_approaches", "datetime_add") 
                        VALUES (?, ?, ?, ?)''', (user_id, number_pullups, number_approaches, datetime.now()))
    conn.commit()



def close():
    """Закрываем соединение с БД"""
    conn.close()