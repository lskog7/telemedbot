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
    current_question = IntegerField(default=0) # Текущий вопрос


class Tests(BaseModel):  # Данные об исследовании
    user_id = ForeignKeyField(Users, null=True)
    date = DateTimeField(null=True)
    add_info = TextField()


class Specialists(BaseModel):  # Данные о специалисте
    info = CharField(max_length=50, null=True)


class Results(BaseModel):  # Результат исследования
    test_id = ForeignKeyField(Tests, null=True)
    specialist_id = ForeignKeyField(Specialists, null=True)


class Questions(BaseModel):  # Вопросы
    text = TextField()


class Answers(BaseModel):  # Вариант ответа
    question_id = ForeignKeyField(Questions)
    answer = CharField(max_length=50)


class UserAnswers(BaseModel):  # Ответы пользователя
    test_id = ForeignKeyField(Tests, null=True)
    answer_id = ForeignKeyField(Answers, null=True)
