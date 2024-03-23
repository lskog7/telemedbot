from peewee import CharField, ForeignKeyField, IntegerField, Model, TextField, SqliteDatabase

# У всех моделей автоматически создается также поле id: PRIMARY KEY AUTOINCREMENT

db = SqliteDatabase('mineralka_new.db')  # Наша бд

# Базовый класс таблицы с прописанной бд, к которой она принадлежит


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
    sex = IntegerField(null=True, choices=SEX_CHOICES, default=0)
    age = IntegerField(null=True)
    result = IntegerField(null=True, default=0)


class Element(BaseModel):  # Хим. элемент
    name = CharField()
    max_grade = IntegerField(null=True)
    edge_grade = IntegerField(null=True)


class Question(BaseModel):  # Вопрос
    text = TextField()


class Answer(BaseModel):  # Вариант ответа
    text = TextField()
    question = ForeignKeyField(Question)


class AnswerElement(BaseModel):
    answer = ForeignKeyField(Answer)
    element = ForeignKeyField(Element)
    grade = IntegerField(default=0)


class UserAnswer(BaseModel):  # Связка варианта ответа и пользователя
    user = ForeignKeyField(User)
    answer = ForeignKeyField(Answer)