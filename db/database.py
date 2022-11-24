from peewee import *
from datetime import datetime

# SQLite database using WAL journal mode and 64MB cache.
db = SqliteDatabase('db/Sport.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})
class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    '''Обьявление таблицы пользовтелей'''
    user_id = PrimaryKeyField(unique=True)
    telegram_id = IntegerField()
    join_date = DateField()
    user_name = CharField(max_length=50)
    user_role = CharField(max_length=50)
    visible = BooleanField(default=True)

    class Meta:
        ORDER_BY = 'user_id'

class TypeExercise(BaseModel):
    '''Обьявление справочника упражнений'''
    name_id = PrimaryKeyField(unique=True)
    name = CharField(max_length=50, unique =True)

    class Meta:
        ORDER_BY = 'name_id'

class Results(BaseModel):
    '''Обьявление таблицы результатов'''
    result_id = PrimaryKeyField(unique=True)
    user_id = ForeignKeyField(Users, to_field='user_id')
    number_pullups = IntegerField(default=0)
    number_approaches = IntegerField(default=0)
    datetime_add = DateField(formats='%Y-%m-%d')
    type_exercise_id = ForeignKeyField(TypeExercise, to_field='name_id', null=True)

    class Meta:
        ORDER_BY = 'result_id'
    # class Meta:
    #     '''Проверка чтобы в одно записи количество раз и подходов были в разумной пределе'''
    #     constraints = [Check('number_pullups between 0 and 100'), Check('number_approaches between 0 and 100')]

def db_exists_table():
    '''Проверка таблиц на существование'''
    db_table_exists_Users()
    db_table_exists_TypeExercise()
    db_table_exists_Results()

def db_table_exists_Users():
    '''Проверка существоваения таблицы User'''
    result = db.table_exists(Users)
    if not result:
        db.create_tables([Users])

def db_table_exists_TypeExercise():
    '''Проверка существоваения таблицы TypeExercise'''
    result = db.table_exists(TypeExercise)
    if not result:
        db.create_tables([TypeExercise])

def db_table_exists_Results():
    '''Проверка существоваения таблицы Results'''
    result = db.table_exists(Results)
    if not result:
        db.create_tables([Results])

def user_registr(user_id, user_name):
    '''Добавляет нового пользователя. Желательно использовать в связке с методом `user_exists`'''
    user = Users(telegram_id=user_id, user_name = user_name, user_role = "user", join_date=datetime.now())
    user.save()

def user_update(user_id, user_name):
    '''Изменение имени пользователя'''
    Users.update(user_name=user_name).where(Users.user_id==user_id)

def user_exists(user_id) -> bool:
    '''Проверка наличия пользователя в бд. Возвращает `True`, если пользователь есть'''
    is_user = Users.select().where(Users.telegram_id==user_id)
    return len(is_user) > 0

def getting_a_name(user_id) -> str:
    '''Получение ника пользователя'''
    user = Users.get(Users.telegram_id==user_id)
    return user.user_name

# def getting_exercises() -> dict:
#     '''Получение списка упражнений'''
#     exercise = TypeExercise.select(TypeExercise)
#     return exercise

# def insert_one_exercises() -> dict:
#     '''Получение списка упражнений'''
#     exercise = TypeExercise(TypeExercise = "Подтягивания")
#     return exercise

# class Update_results:
#     def checking_the_record_exercises_db(user_id, exercises):
#         '''Проверка на существование записи пользователя с вырбранным упражнением и сегодняшним днем'''
#         result = Results.get(Results.user_id == user_id and Results.type_exercise_id == TypeExercise.get(TypeExercise.name==exercises) and Results.datetime_add == datetime.now())
#         return result
    
#     def insert_the_record_exercises_db(user_id, exercises):
#         '''Добавление новой записи result'''
#         results = Results(user_id=user_id, type_exercise_id = TypeExercise.get(TypeExercise.name==exercises), datetime_add=datetime.now())
#         results.save()

#     def results_update_number_of_times_db(user_id, number_of_times, exercises):
#         '''Обновление результатов'''
#         Results.update(number_of_times=+number_of_times).where(Results.user_id == user_id and Results.type_exercise_id == TypeExercise.get(TypeExercise.name==exercises) and Results.datetime_add == datetime.now())

#     def results_update_number_approaches_db(user_id, number_approaches, exercises):
#         Results.update(number_approaches=+number_approaches).where(Results.user_id == user_id and Results.type_exercise_id == TypeExercise.get(TypeExercise.name==exercises) and Results.datetime_add == datetime.now())

def checking_the_record_exercises_db(user_id):
    '''Проверка на существование записи пользователя с сегодняшней датой'''
    user_id = Users.get(Users.telegram_id == user_id)
    result = Results.select().where(Results.user_id == user_id.user_id and Results.type_exercise_id == 1 and Results.datetime_add == datetime.now())
    return result
    
def insert_the_record_exercises_db(user_id):
    '''Добавление новой записи result'''
    user_id = Users.get(Users.telegram_id == user_id)
    results = Results(user_id=user_id.user_id, type_exercise_id = 1, datetime_add=datetime.now())
    results.save()

def results_update_number_pullups_db(user_id, number):
    '''Обновление результатов по количеству'''
    user_id = Users.get(Users.telegram_id == user_id)
    results = Results.get(Results.user_id == user_id.user_id and Results.type_exercise_id == 1 and Results.datetime_add == datetime.now())
    number_pullups = results.number_pullups + int(number)

    results = Results.update(number_pullups=+number_pullups).where(Results.user_id == results.user_id and Results.type_exercise_id == 1 and Results.datetime_add == datetime.now())
    results.execute()

def results_update_number_approaches_db(user_id, number):
    '''Обновление результатов по подходам'''
    user_id = Users.get(Users.telegram_id == user_id)
    results = Results.get(Results.user_id == user_id.user_id and Results.type_exercise_id == 1 and Results.datetime_add == datetime.now())
    number_approaches = results.number_approaches + int(number)

    results = Results.update(number_approaches=number_approaches).where(Results.user_id == results.user_id and Results.type_exercise_id == 1 and Results.datetime_add == datetime.now())
    results.execute()

def select_rating_day():
    #results = Results.select(Users.user_name, TypeExercise.name, Results.number_pullups, Results.number_approaches, Results.datetime_add).join_from(Results, Users, JOIN.NATURAL).join_from(Results, TypeExercise, JOIN.NATURAL)
    rating = Results.select().join(Users).join(TypeExercise).orderby(Results.number_pullups)
    print(rating)

def select_rating_month():
    pass

def select_rating_year():
    pass