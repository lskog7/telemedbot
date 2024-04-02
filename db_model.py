from peewee import (
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
    DateTimeField,
    SqliteDatabase,
)

# У всех моделей автоматически создается также поле id: PRIMARY KEY AUTO_INCREMENT

db = SqliteDatabase("telehack.db")  # Наша бд


class BaseModel(Model):
    class Meta:
        database = db


# -------------------------------Таблицы--------------------------------


class Users(BaseModel):  # Пользователь
    SEX_CHOICES = ((0, "Не указан"), (1, "Мужской"), (2, "Женский"))

    telegram_id = IntegerField(unique=True)
    sex = IntegerField(null=True, choices=SEX_CHOICES, default=0)
    name = CharField(max_length=256)
    surname = CharField(max_length=256)
    patronymic = CharField(max_length=256)
    b_date = DateTimeField()
    current_test = IntegerField(default=0)
    current_question = IntegerField(default=0)  # Текущий вопрос


class Tests(BaseModel):  # Данные об исследовании
    user_id = ForeignKeyField(Users, null=True)
    date = DateTimeField()
    add_info = TextField(default=0)


class Specialists(BaseModel):  # Данные о специалисте
    name = TextField(default=0)
    info = TextField(default=0)


class Results(BaseModel):  # Результат исследования
    test_id = ForeignKeyField(Tests)
    specialist_id = ForeignKeyField(Specialists)


class Questions(BaseModel):  # Вопросы
    text = TextField(default=0)
    type = IntegerField(default=0)  # Тип: 0 - закрытый ответ, 1 - открытый ответ



class Answers(BaseModel):  # Вариант ответа
    question_id = ForeignKeyField(Questions, null=True)
    answer = TextField(default=0)
    type = IntegerField(default=0)
    score = IntegerField(default=0)


class UserAnswers(BaseModel):  # Ответы пользователя
    user_id = IntegerField()
    test_id = IntegerField()
    question_id = IntegerField()
    answer_id = IntegerField()
    score = IntegerField()
    free_answer = TextField(default=0)
