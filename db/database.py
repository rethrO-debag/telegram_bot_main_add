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
    user_id = IntegerField()
    join_date = DateField()
    user_name = CharField(max_length=50)
    user_role = CharField(max_length=50)
    visible = BooleanField(default=True)

class TypeExercise(BaseModel):
    '''Обьявление справочника упражнений'''
    name = CharField(max_length=50)

class Results(BaseModel):
    '''Обьявление таблицы результатов'''
    user_id = ForeignKeyField(Users, backref='results')
    number_of_times = IntegerField(default=0)
    number_approaches = IntegerField(default=0)
    datetime_add = DateField(formats='%Y-%m-%d')
    type_exercise_id = ForeignKeyField(TypeExercise, backref='results', null=True)

    class Meta:
        '''Проверка чтобы в одно записи количество раз и подходов были в разумной пределе'''
        constraints = [Check('number_pullups between 0 and 100'), Check('number_approaches between 0 and 100')]

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
    user = Users(user_id=user_id, user_name = user_name, user_role = "user", join_date=datetime.now())
    user.save()

def user_update(user_id, user_name):
    '''Изменение имени пользователя'''
    Users.update(user_name=user_name).where(Users.user_id==user_id)

def user_exists(user_id) -> bool:
    '''Проверка наличия пользователя в бд. Возвращает `True`, если пользователь есть'''
    is_user = Users.select().where(Users.user_id==user_id)
    return len(is_user) > 0

def getting_a_name(user_id) -> str:
    '''Получение ника пользователя'''
    user = Users.select().where(Users.user_id==user_id)
    return user.user_name

def getting_exercises() -> dict:
    '''Получение списка упражнений'''
    exercise = TypeExercise.select(TypeExercise)
    return exercise

class Update_results:
    def checking_the_record_exercises_db(user_id, exercises_id):
        '''Проверка на существование записи пользователя с вырбранным упражнением и сегодняшним днем'''
        result = Results.select().where(Results.user_id == user_id and Results.type_exercise_id == exercises_id and Results.datetime_add == datetime.now())
        return result
    
    def insert_the_record_exercises_db(user_id, exercises_id):
        '''Добавление новой записи result'''
        results = Results(user_id=user_id, type_exercise_id = exercises_id, datetime_add=datetime.now(), number_of_times = 0, number_approaches=0)
        results.save()

    # def results_update_number_of_times_db(user_id, number_of_times):
    #     '''Обновление результатов'''
    #     Results.update(number_of_times=+number_of_times).where(Results.user_id == user_id and Results.type_exercise_id == exercises_id and Results.datetime_add == datetime.now())

    # def results_update_number_approaches_db(user_id, number_approaches):
    #     Results.update(number_approaches=+number_approaches).where(Results.user_id == user_id and Results.type_exercise_id == exercises_id and Results.datetime_add == datetime.now())