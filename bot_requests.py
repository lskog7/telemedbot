from db_model import Users, Tests, Specialists, Results, Questions, Answers, UserAnswers
from peewee import JOIN
from datetime import datetime
from sim_crypto import encrypt, decrypt


class Requests:

    # Проверка наличия пользователя в БД по id
    @staticmethod
    def users_in_db(telegram_id):
        count = Users.select(Users.telegram_id).where(Users.telegram_id == telegram_id).count()
        return count

    # Запись новой строки в таблицу users
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
    def get_user_name(telegram_id, key, iv):
        query = Users.select().where(Users.telegram_id == telegram_id)
        return decrypt(query[0].name, key, iv)

    # Возвращает фамилию выбранного пользователя
    @staticmethod
    def get_user_surname(telegram_id, key, iv):
        query = Users.select().where(Users.telegram_id == telegram_id)
        return decrypt(query[0].surname, key, iv)

    # Возвращает отчество выбранного пользователя
    @staticmethod
    def get_user_patronymic(telegram_id, key, iv):
        query = Users.select().where(Users.telegram_id == telegram_id)
        return decrypt(query[0].patronymic, key, iv)

    # Возвращает дату рождения выбранного пользователя
    @staticmethod
    def get_user_b_date(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        return query[0].b_date.date()

    # Сохраняет имя пользователя
    @staticmethod
    def save_user_name(telegram_id, name, key, iv):
        query = Users.get(Users.telegram_id == telegram_id)
        query.name = encrypt(name, key, iv)
        query.save()

    # Сохраняет фамилия пользователя
    @staticmethod
    def save_user_surname(telegram_id, surname, key, iv):
        query = Users.get(Users.telegram_id == telegram_id)
        query.surname = encrypt(surname, key, iv)
        query.save()

    # Сохраняет отчество пользователя
    @staticmethod
    def save_user_patronymic(telegram_id, patronymic, key, iv):
        query = Users.get(Users.telegram_id == telegram_id)
        query.patronymic = encrypt(patronymic, key, iv)
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

    # Возвращает список результатов пользователя (id специалистов)
    @staticmethod
    def get_user_result(telegram_id, test_num):
        user_tests = Requests.get_user_tests(telegram_id)
        if user_tests != -1:
            if len(user_tests) < test_num:
                query = Results.select(Results.specialist_id).where(
                    Results.test_id == user_tests[test_num]
                )
                specialists_ids = []
                for spec in query:
                    specialists_ids.append(spec.specialist_id)
                return specialists_ids
            else:
                return -1
        else:
            return -1

    # Возвращает описание специалистов по id
    @staticmethod
    def get_specialists_info(specialists_ids):
        specialists_info = []
        for id in specialists_ids:
            query = Specialists.select(Specialists.info).where(Specialists.id == id)
            info = query[0].info
            specialists_info.append(info)
        return specialists_info

    # Возвращает описание специалистов для выбранного юзера и выбранного теста
    @staticmethod
    def get_user_specialists(telegram_id, test_num):
        specialists_ids = Requests.get_user_result(telegram_id, test_num)
        specialists_info = Requests.get_specialists_info(specialists_ids)
        return specialists_info

    @staticmethod
    def get_user_info(telegram_id, key, iv):
        query = Users.select().where(Users.telegram_id == telegram_id)
        if len(query) != 0:
            user = query[0]
            info = [0 for _ in range(5)]
            info[0] = decrypt(user.name, key, iv)
            info[1] = decrypt(user.surname, key, iv)
            info[2] = decrypt(user.patronymic, key, iv)
            info[3] = Users.SEX_CHOICES[user.sex][1]
            info[4] = user.b_date.date()
            return info
        else:
            return -1

    @staticmethod
    def start_new_test(telegram_id, text_info=""):
        query1 = Users.select().where(Users.telegram_id == telegram_id)
        user_id = query1[0].id
        query2 = Tests(user_id=user_id, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text=text_info, curr_test=0)
        query2.save()