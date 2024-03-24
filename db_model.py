from peewee import CharField, ForeignKeyField, IntegerField, Model, TextField, DateTimeField, SqliteDatabase

# У всех моделей автоматически создается также поле id: PRIMARY KEY AUTOINCREMENT

db = SqliteDatabase('telehack.db')  # Наша бд

class BaseModel(Model):
    class Meta:
        database = db

# -------------------------------Таблицы--------------------------------

class User(BaseModel):  # Пользователь
    SEX_CHOICES = (
        (0, 'Мужской'),
        (1, 'Женский'),
        (2, 'Не указан')
    )

    telegram_id = IntegerField(unique=True)
    sex = IntegerField(null=True, choices=SEX_CHOICES, default=2)
    name = CharField(max_length=30)
    surname = CharField(max_length=30)
    age = DateTimeField()


class Test(BaseModel):  # Данные об исследовании
    user_id = ForeignKeyField(User, null=True)
    date = DateTimeField(null=True)
    text_info = TextField()


class Specialist(BaseModel): # Данные о специалисте
    field = CharField(max_length=50, null=True)


class Result(BaseModel): # Результат исследования
    test_id = ForeignKeyField(Test, null=True)
    specialist_id = ForeignKeyField(Specialist, null=True)


class Question(BaseModel):  # Вопрос
    text = TextField()


class Answer(BaseModel):  # Вариант ответа
    text = TextField()
    question = ForeignKeyField(Question)


class UserAnswer(BaseModel):  # Связка варианта ответа и исследования
    test_id = ForeignKeyField(Test, null=True)
    answer_id = ForeignKeyField(Answer, null=True)
