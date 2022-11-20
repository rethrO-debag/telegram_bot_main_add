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
    visible = BooleanField(default=True)

class TypeExercise(BaseModel):
    '''Обьявление справочника упражнений'''
    name = CharField(max_length=50)

class IntermediateTable(BaseModel):
    '''Промежуточная таблица для хранения количества подходов'''
    user_id = ForeignKeyField(Users, backref='results')
    number_pullups = IntegerField(default=0)
    datetime_add = DateField(formats='%Y-%m-%d')
    type_exercise_id = ForeignKeyField(TypeExercise, backref='results', null=True)

class Results(BaseModel):
    '''Обьявление таблицы результатов'''
    user_id = ForeignKeyField(Users, backref='results')
    number_pullups = IntegerField(default=0)
    number_approaches = IntegerField(default=0)
    datetime_add = DateField(formats='%Y-%m-%d')
    type_exercise_id = ForeignKeyField(TypeExercise, backref='results', null=True)

    class Meta:
        '''Проверка чтобы в одно записи количество раз и подходов были в разумной пределе'''
        constraints = [Check('number_pullups between 0 and 100'), Check('number_approaches between 0 and 100')]

def db_conn():
    '''Создание таблиц'''
    db.create_tables([Results, TypeExercise, Users, IntermediateTable])

def user_registr(user_id, user_name):
    '''Добавляет нового пользователя. Желательно использовать в связке с методом `user_exists`'''
    user = Users(user_id=user_id, user_name = user_name, join_date=datetime.now())
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
    for user in Users.select().where(Users.user_id==user_id):
        return user.user_name

def getting_exercises() -> dict:
    '''Получение списка упражнений'''
    exercise = TypeExercise.select()
    return exercise

def Insert_number_pullups(user_id, pullups):
    '''Добавление в промежуточную таблицу количество раз'''
    if not user_exists(user_id=user_id):
        print(f'Пользователь {user_id} в базе не найден')
        user_registr(tg_user_id=user_id)
        print(f'Добавили {user_id}')
    user = Users.get(Users.user_id==user_id)


    pllps = IntermediateTable(user_id=user.id, number_pullups=pullups, datetime_add=datetime.now())
    pllps.save()


