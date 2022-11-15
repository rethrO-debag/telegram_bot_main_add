from sqlite import Database
from config import msgs

db = Database()

# Здесь будем прописывать логику маломальскую, 
# данный файл называют ещё core.py
# Как я понял у тебя он назывался логик

def firstMSG(userId)-> str:
    '''Проверка наличия пользователя, ежи нет добавляем'''
    if not db.user_exists(userId):
        db.auth_user(userId)
        return msgs['neofit']
    else:
        return msgs['firstMSG']

def exercises_button():
    db.select_exercises()