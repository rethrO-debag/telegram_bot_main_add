from config import msgs
import db.database as db

def table_exists():
    '''При запуске проверка на существование таблиц в базе данных'''
    db.db_exists_table

def user_verification(userId)-> str:
    '''Проверка пользователя по базе, если нету то регистрируем'''
    if not db.user_exists(userId):
        return msgs['registr']
    else:
        return msgs['return']

def user_register(userId, user_name):
    '''Регистрация нового пользователя'''
    db.user_registr(userId, user_name)
    return msgs['welcome']

def user_name(userId):
    '''Запрос имени пользователя, который пользователь установил для себя'''
    user_name = db.getting_a_name(userId)
    return user_name
    
def update_user_name(userId, user_name):
    '''Изменение имени пользователя'''
    db.user_update(userId, user_name)

def exercises():
    '''Получение списка упражнений'''
    exercise =[]
    button_exercise = db.getting_exercises()
    for button in button_exercise:
        exercise.append(button.name)
    return exercise

def checking_the_record(user_id, exercises):
    exercise =[]
    button_exercise = db.getting_exercises()
    for button in button_exercise:
        exercise.append(button.name)
    return exercise

    result_user = db.checking_the_record_db(user_id, exercises)
    if not db.checking_the_record_db(user_id):
        button_exercise1 =[]
        return 