from db_model import Users, Tests, Specialists, Results, Questions, Answers, UserAnswers
from peewee import JOIN
import datetime


class Requests:

    # Проверка наличия пользователя в БД по id
    @staticmethod
    def users_in_db(telegram_id):
        count = Users.select(Users.telegram_id).where(Users.telegram_id == telegram_id).count()
        return count

    # Запись юзера
    @staticmethod
    def write_user(telegram_id):
        # Записываем новую строчку в БД
        query = Users(telegram_id=telegram_id, sex=0)
        query.save()

    # Возвращает пол выбранного пользователя
    @staticmethod
    def get_user_sex(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        return Users.SEX_CHOICES[query[0].sex][1]

    # Возвращает имя выбранного пользователя
    @staticmethod
    def get_user_name(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        return query[0].name

    # Возвращает фамилию выбранного пользователя
    @staticmethod
    def get_user_surname(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        return query[0].surname

    # Возвращает отчество выбранного пользователя
    @staticmethod
    def get_user_patronymic(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        return query[0].patronymic

    # Возвращает дату рождения выбранного пользователя
    @staticmethod
    def get_user_b_date(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        return query[0].b_date

    # Сохраняет имя пользователя
    @staticmethod
    def save_user_name(telegram_id, name):
        query = Users.get(Users.telegram_id == telegram_id)
        query.name = name
        query.save()

    # Сохраняет фамилия пользователя
    @staticmethod
    def save_user_surname(telegram_id, surname):
        query = Users.get(Users.telegram_id == telegram_id)
        query.surname = surname
        query.save()

    # Сохраняет отчество пользователя
    @staticmethod
    def save_user_patronymic(telegram_id, patronymic):
        query = Users.get(Users.telegram_id == telegram_id)
        query.patronymic = patronymic
        query.save()

    # Сохраняет пол пользователя
    @staticmethod
    def save_user_sex(telegram_id, sex):
        query = Users.get(Users.telegram_id == telegram_id)
        query.sex = sex
        query.save()

    # Сохраняет дату рождения пользователя
    @staticmethod
    def save_user_b_date(telegram_id, date_str):
        query = Users.get(Users.telegram_id == telegram_id)
        query.b_date = date_str
        query.save()

    # Возвращает номер последнего теста и вопроса для пользователя (если нет, то 0, 0)
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

    # Возвращает текст вопроса
    @staticmethod
    def get_question_text(question_id):  # Очередной неотвеченный вопрос
        query = Questions.select().where(Questions.id == question_id)
        if len(query) != 0:
            text = query[0].text
            return text
        else:
            return -1

    # Возвращает варианты ответа на вопрос
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

    # Очередной неотвеченный вопрос (номер) и его варианты ответа (лист)
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

    # Возвращает список тестов пользователя
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
            info = [0 for _ in range(5)]
            info[0] = user.name
            info[1] = user.surname
            info[2] = user.patronymic
            info[3] = user.sex
            info[4] = user.b_date
            return info
        else:
            return -1

    @staticmethod
    def start_new_test(telegram_id, text_info=""):
        query1 = Users.select().where(Users.telegram_id == telegram_id)
        user_id = query1[0].id
        query2 = Tests(user_id=user_id, date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text=text_info, curr_test=0)
        query2.save()