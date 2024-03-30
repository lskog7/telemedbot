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
        query = Users.select().where(Users.telegram_id == telegram_id)
        current_test = query[0].current_test
        current_question = query[0].current_question
        if current_test != 0:
            if current_question == 0:
                return current_test, 0
            else:
                return current_test, current_question
        else:
            return 0, 0

    @staticmethod
    def get_question_text(question_id):  # Очередной неотвеченный вопрос
        query = Questions.select().where(Questions.id == question_id)
        if len(query) != 0:
            text = query[0].text
            return text
        else:
            return -1

    @staticmethod
    def get_question_answers(question_id):  # Все варианты ответов на вопрос
        query = Answers.select().where(Answers.question_id == question_id)
        if len(query) != 0:
            answers = []
            for answer in query:
                answers.append(answer)
            return answers
        else:
            return -1

    # Очередной неотвеченный вопрос и его варианты ответа
    @staticmethod
    def get_next_user_question_and_answers(telegram_id):
        current_test, current_question = Requests.get_user_next_question(telegram_id)
        if current_test != 0 and current_question != 0:
            question_text = Requests.get_question_text(current_question)
            question_answers = Requests.get_question_answers(current_question)
            return question_text, question_answers
        elif current_test != 0 and current_question == 0:
            first_question_text = Requests.get_question_text(1)
            first_question_answers = Requests.get_question_answers(1)
            return first_question_text, first_question_answers
        else:
            return -1, -1

    @staticmethod
    def get_user_tests(telegram_id):
        query1 = Users.select(Users.id).where(Users.telegram_id == telegram_id)
        if len(query1) == 0:
            return -1
        user_id = query1[0].id
        query2 = Tests.select(Tests.id).where(Tests.user_id == user_id)
        if len(query2) == 0:
            return -1
        test_ids = []
        for t_id in query2:
            test_ids.append(t_id)
        return test_ids

    @staticmethod
    def get_user_result(telegram_id, test_num):
        user_tests = Requests.get_user_tests(telegram_id)
        if user_tests != -1:
            if len(user_tests) < test_num:
                query = Results.select(Results.specialist_id).where(
                    Results.test_id == user_tests[test_num]
                )
                specialists = []
                for spec in query:
                    specialists.append(spec)
                return specialists
            else:
                return -1
        else:
            return -1

    @staticmethod
    def get_user_info(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        if len(query) != 0:
            user = query[0]
            info = [0 i in range(7)]
            info[0] = user.id
            info[1] = user.telegram_id
            info[2] = user.name
            info[3] = user.surname
            info[4] = user.patronymic
            info[5] = user.sex
            info[6] = user.b_date
            return info
        else:
            return -1
