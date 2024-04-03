from peewee import (
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
    DateTimeField,
    SqliteDatabase,
)

# У всех моделей автоматически создается также поле id: PRIMARY KEY AUTO_INCREMENT


# --------------------------------Используемая база данных--------------#
db = SqliteDatabase("telehack.db")  #


class BaseModel(Model):
    class Meta:
        database = db


# -----------------------------------------------------------------------#
# --------------------------------Таблицы--------------------------------#
# -----------------------------------------------------------------------#


# --------------------------------Данные о пользователях-----------------#
class Users(BaseModel):
    SEX_CHOICES = ((0, "Не указан"), (1, "Мужской"), (2, "Женский"))
    telegram_id = IntegerField(null=True, unique=True)  # Айди телеграма пользователя, уникальная штука
    sex = IntegerField(null=True, choices=SEX_CHOICES, default=0)  # Пол пользователя
    name = TextField()  # Имя пользователя
    surname = TextField()  # Фамилия пользователя
    patronymic = TextField()  # Отчество пользователя
    b_date = DateTimeField()  # Дата рождения пользователя
    current_test = IntegerField(default=0)  # Текущий тест, который проходит пользователь
    # current_question = IntegerField(default=0)  # Текущий вопрос, на который отвечает полльзователь


# --------------------------------Данные о тестах------------------------#
class Tests(BaseModel):
    user_id = ForeignKeyField(Users, null=True)  # Айди пользователя, который проходит тест
    date = DateTimeField()  # Дата начала выполнения теста
    # add_info = TextField(default=0) # Дополнительная информация
    status = IntegerField(default=0)  # 0 - если тест активен, 1 - если тест завершен
    qtables = TextField(default=0)  # Список таблиц вопросов, которые необходимо пройти пользователю помимо основной
    curqtable = TextField(default=0)  # Такущая таблица из дополнительных, в которой сидит пользователь
    curq = IntegerField(default=0)  # Текущий вопрос из текущей таблицы


# --------------------------------Данные о специалистах------------------#
class Specialists(BaseModel):
    name = TextField(default=0)  # Название специалиста
    info = TextField(default=0)  # Описание сферы деятельности


# --------------------------------Данные о результатах тестов------------#
class Results(BaseModel):
    test_id = ForeignKeyField(Tests)  # Айди теста, которому соответствует результат
    specialist_id = ForeignKeyField(Specialists)  # Айди специалиста, к которому надо пойти


# --------------------------------Вопросы по хирургии--------------------#
class Qsurgery(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)


# --------------------------------Вопросы по кардиологии-----------------#
class Qcardio(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)


# --------------------------------Вопросы по дерматологии----------------#
class Qdermo(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)


# --------------------------------Вопросы по эндокринологии--------------#
class Qendo(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Вопросы по гастроэнтерологии-----------#
class Qgastro(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Общие вопросы--------------------------#
class Qgeneral(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Вопросы по гинекологии-----------------#
class Qgyne(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Вопросы по ЛОР-------------------------#
class Qlor(BaseModel):  # Вопросы по ЛОР
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Вопросы по неврологии------------------#
class Qnevro(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Вопросы по офтальмологии---------------#
class Qofta(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Вопросы по пульманологии---------------#
class Qpulmo(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Вопросы по стоматологии----------------#
class Qstom(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Вопросы по психиатрии------------------#
class Qsycho(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Вопросы по урологии------------------#
class Quro(BaseModel):
    text = TextField(default=0)  # Текст вопроса
    type = IntegerField(default=0)  # Тип: 0-2 (0-да/нет, 1-варианты, 2-свободный)
    score = IntegerField(default=0)

# --------------------------------Данные об ответах на вопросы-----------#
class Answers(BaseModel):
    qtable = TextField(null=True)  # К какой таблице вопросов принадлежит вопрос
    qid = IntegerField(null=True)  # Айди вопроса в его таблице (по сути порядковый номер)
    answer = TextField(default=0)  # Вариант ответа на вопрос
    type = IntegerField(default=0)  # Тип вопроса 0-2
    score = TextField(default=0)  # Количество баллов за данный вопрос


# --------------------------------Данные об ответах пользователя---------#
class Useranswers(BaseModel):
    user_id = IntegerField()  # Айди пользователя, которому принадлежит ответ
    test_id = IntegerField()  # Айди теста, к которому принадлежит ответ
    table_id = TextField()  # Название таблицы к которой принадлежит вопрос
    question_id = IntegerField()  # Айди вопроса из соответствующей таблицы
    answer_id = IntegerField()  # Айди ответа
    score = IntegerField(default=0)  # Счет, подтягивается из ответа
    free_answer = TextField(default=0)  # В это поле записывается свободный ответ
