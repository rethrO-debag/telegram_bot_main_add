# import db.db_old as db_old, db.database as dbModel
from config import msgs
import db.database as db


# Здесь будем прописывать логику маломальскую, 
# данный файл называют ещё core.py
# Как я понял у тебя он назывался логик

# def firstMSG(userId)-> str:
#     return msgs['neofit']
#     # '''Проверка наличия пользователя, ежи нет добавляем'''
#     # if not db_old.user_exists(userId):
#     #     db_old.auth_user(userId)
#     #     return msgs['neofit']
#     # else:
#     #     return msgs['firstMSG']

def user_verification(userId)-> str:
    #Проверка наличия пользователя, ежи нет добавляем
    if not db.user_exists(userId):
        return msgs['registr']
    else:
        return msgs['return']

def user_register(userId, user_name):
    db.user_registr(userId, user_name)
    return msgs['welcome']