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
    name = CharField()
    surname = CharField
    age = IntegerField()


class Test(BaseModel):  # данные об исследовании
    user_id = ForeignKeyField(User, null=True)
    date = DateTimeField(null=True)
    text_info = TextField()

