from typing import Self
from db_model import Users, Tests, Specialists, Results, Questions, Answers, UserAnswers
from peewee import JOIN


class Requests:

    @staticmethod
    def users_in_db(user):
        return Users.select(Users.telegram_id).count()

    @staticmethod
    def write_user(telegram_id):
        u = Users(telegram_id=telegram_id, sex=0)
        u.save()

    @staticmethod
    def user_sex(telegram_id):
        u = Users.select().where(Users.telegram_id == telegram_id)
        return Users.SEX_CHOICES[u[0].sex][1]

    @staticmethod
    def user_name(telegram_id):
        u = Users.select().where(Users.telegram_id == telegram_id)
        return u[0].name

    @staticmethod
    def user_surname(telegram_id):
        u = Users.select().where(Users.telegram_id == telegram_id)
        return u[0].surname

    @staticmethod
    def user_patronymic(telegram_id):
        u = Users.select().where(Users.telegram_id == telegram_id)
        return u[0].patronymic

    @staticmethod
    def user_b_date(telegram_id):
        u = Users.select().where(Users.telegram_id == telegram_id)
        return u[0].b_date

    @staticmethod
    def save_user_name(telegram_id, name):
        u = Users.get(Users.telegram_id == telegram_id)
        u.name = name
        u.save()

    @staticmethod
    def save_user_surname(telegram_id, surname):
        u = Users.get(Users.telegram_id == telegram_id)
        u.surname = surname
        u.save()

    @staticmethod
    def save_user_patronymic(telegram_id, patronymic):
        u = Users.get(Users.telegram_id == telegram_id)
        u.patronymic = patronymic
        u.save()

    @staticmethod
    def save_user_sex(telegram_id, sex):
        u = Users.get(Users.telegram_id == telegram_id)
        u.sex = sex
        u.save()

    @staticmethod
    def save_user_b_date(telegram_id, date_str):
        u = Users.get(Users.telegram_id == telegram_id)
        u.b_date = date_str
        u.save()

    @staticmethod
    def get_user_next_question(telegram_id):  # Очередной неотвеченный вопрос
        query = Users.select().where(Users.telegram_id == telegram_id)[0]
        current_test = query.current_test
        current_question = query.current_question
        if current_test != 0:
            if current_question == 0:
                return current_test, 0
            else:
                return current_test, current_question
        else:
            return 0, 0

    @staticmethod
    def get_question_text(question_id):  # Очередной неотвеченный вопрос
        query = Questions.select().where(Questions.id == question_id)[0]
        text = query.text
        return text

    @staticmethod
    def get_question_answers(question_id):  # Все варианты ответов на вопрос
        query = Answers.select().where(Answers.question_id == question_id)
        answers = []
        for answer in query:
            answers.append(answer)
        return answers

    # Очередной неотвеченный вопрос и его варианты ответа
    @staticmethod
    def get_next_user_question_and_answers(telegram_id):
        current_test, current_question = Requests.get_user_next_question(telegram_id)
        question_text = Requests.get_question_text(current_question)
        question_answers = Requests.get_question_answers(current_question)
        return question_text, question_answers
