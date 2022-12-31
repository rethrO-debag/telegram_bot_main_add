from peewee import *
from datetime import datetime
from loguru import logger

# SQLite database using WAL journal mode and 64MB cache.
db = SqliteDatabase('db/Sport.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class Users(BaseModel):
    '''Обьявление таблицы пользовтелей'''
    telegram_id = IntegerField()
    join_date = DateField()
    user_name = CharField(max_length=50)
    user_role = CharField(max_length=50)
    visible = BooleanField(default=True)

    class Meta:
        db_table = 'users'


class TypeExercise(BaseModel):
    '''Обьявление справочника упражнений'''
    name = CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'TypeExercise'


class Results(BaseModel):
    '''Обьявление таблицы результатов'''
    user_id = ForeignKeyField(Users)
    number_pullups = IntegerField(default=0)
    number_approaches = IntegerField(default=0)
    datetime_add = DateField(formats='%Y-%m-%d')
    type_exercise_id = ForeignKeyField(TypeExercise)

    class Meta:
        db_table = 'results'


def db_exists_table():
    '''Проверка таблиц на существование'''
    logger.info("Запуск процедуры проверки таблиц в базе данных")
    db_table_exists()


def db_table_exists():
    tables = [Users, TypeExercise, Results]
    if not all(table.table_exists() for table in tables):
        db.create_tables(tables)
        logger.debug('Таблицы созданы успешно.')
    else:
        logger.debug('Таблицы уже существуют.')


def user_registr(user_id, user_name):
    '''Добавляет нового пользователя. Желательно использовать в связке с методом `user_exists`'''
    user = Users(telegram_id=user_id, user_name=user_name,
                 user_role="user", join_date=datetime.now())
    logger.debug("Ввод данных нового пользователя.")
    user.save()


def user_update(telegram_id, now_name):
    '''Изменение имени пользователя'''
    old_name = Users.get(telegram_id=telegram_id)
    result = Users.update(user_name=now_name).where(id)
    logger.info("Изменение имени пользователя: " + str(id) + ". Старое имя: \"" +
                old_name.user_name + "\" на \"" + str(now_name) + "\"")
    result.execute()


def user_exists(user_id) -> bool:
    '''Проверка наличия пользователя в бд. Возвращает `True`, если пользователь есть'''
    is_user = Users.select().where(Users.telegram_id == user_id)
    return len(is_user) > 0


def getting_a_name(user_id) -> str:
    '''Получение ника пользователя'''
    user = Users.get(Users.telegram_id == user_id)
    logger.info("Получение ника пользователя: " + str(user_id))
    return user.user_name


def checking_the_record_exercises_db(user_id):
    '''Проверка на существование записи пользователя с сегодняшней датой'''
    user_id = Users.get(Users.telegram_id == user_id)
    result = Results.select().where(Results.user_id == user_id.id and Results.type_exercise_id ==
                                    1 and Results.datetime_add == datetime.now())
    logger.debug("Вывод данных")

    return result


def insert_the_record_exercises_db(user_id):
    '''Добавление новой записи result'''
    user_id = Users.get(Users.telegram_id == user_id)
    results = Results(user_id=user_id.id, type_exercise_id=1,
                      datetime_add=datetime.now())
    logger.debug("Ввод данных")
    results.save()


def results_update_number_pullups_db(user_id, number):
    '''Обновление результатов по количеству'''
    user_id = Users.get(Users.telegram_id == user_id)
    results = Results.get(Results.user_id == user_id.id and Results.type_exercise_id ==
                          1 and Results.datetime_add == datetime.now())
    number_pullups = results.number_pullups + int(number)

    results = Results.update(number_pullups=+number_pullups).where(Results.user_id ==
                                                                   results.user_id and Results.type_exercise_id == 1 and Results.datetime_add == datetime.now())
    logger.debug("Ввод данных")
    results.execute()


def results_update_number_approaches_db(user_id, number):
    '''Обновление результатов по подходам'''
    try:
        user_id = Users.get(Users.telegram_id == user_id)
        results = Results.get(Results.user_id == user_id.id and Results.type_exercise_id ==
                              1 and Results.datetime_add == datetime.now())
        number_approaches = results.number_approaches + int(number)

        results = Results.update(number_approaches=number_approaches).where(
            Results.user_id == results.user_id and Results.type_exercise_id == 1 and Results.datetime_add == datetime.now())
        results.execute()
        logger.debug("Результаты по подходам обновленны.")
    finally:
        logger.error(
            "Ошибка обновления результатов по подходам. Данные не сохранены!")


def select_rating_day():
    rating = Results.select().where(Results.datetime_add == datetime.now()
                                    ).order_by(Results.number_pullups.desc())
    logger.debug("Получение данных за день.")

    return rating


def select_rating_month():
    rating = Results.select().where(fn.date_part('month', Results.datetime_add) ==
                                    datetime.now().month).order_by(Results.number_pullups.desc())
    logger.debug("Получение данных за месяц.")

    return rating


def select_rating_year():
    rating = Results.select().where(fn.date_part('year', Results.datetime_add) ==
                                    datetime.now().year).order_by(Results.number_pullups.desc())
    logger.debug("Получение данных за год.")

    return rating
