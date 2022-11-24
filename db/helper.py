from config import msgs
import db.database as db

def table_exists():
    '''При запуске проверка на существование таблиц в базе данных'''
    db.db_exists_table()

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

# def exercises():
#     '''Получение списка упражнений'''
#     exercise =[]
#     global button
#     button_exercise = db.getting_exercises()
#     for button in button_exercise:
#         exercise.append(button.name)
#     return exercise

def check_result(user_id):
    '''Изменение имени пользователя'''
    if not db.checking_the_record_exercises_db(user_id):
        db.insert_the_record_exercises_db(user_id)

def update_number_pullups(user_id, number_pullups):
    db.results_update_number_pullups_db(user_id, number_pullups)

def update_number_approaches(user_id, number_approaches):
    db.results_update_number_approaches_db(user_id, number_approaches)

def select_rating(rating):
    db.select_rating_day()