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
    def start_new_test(telegram_id):
        query1 = Users.select().where(Users.telegram_id == telegram_id)
        user_id = query1[0].id
        query2 = Tests(user_id=user_id, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), curr_test=0)
        query2.save()

    # Функция, которая возвращает список всех вопросов и всех ответов
    # questions[индекс вопроса][0 - id
    #                           1 - тест вопроса
    #                           2 - массив ответов][итерации по ответам, если ранее - 2]
    @staticmethod
    def get_full_question_list():
        query1 = Questions.select().where(Questions.type != 3)
        questions = []
        for q in query1:
            if q.type != 3:
                if q.type == 0:
                    ans = ["Да", "Нет"]
                    tmp = [q.id, q.text, ans]
                    questions.append(tmp)
                elif q.type == 1:
                    query2 = Answers.select().where(Answers.question_id == q.id)
                    ans = []
                    for q2 in query2:
                        ans.append(q2.answer)
                    tmp = [q.id, q.text, ans]
                    questions.append(tmp)
                elif q.type == 2:
                    ans = ["Введите ответ"]
                    tmp = [q.id, q.text, ans]
                    questions.append(tmp)
        return questions

    # Список id вопросов по порядку
    @staticmethod
    def get_question_ids():
        query = Questions.select(Questions.id).where(Questions.type != 3)
        question_ids = []
        for question in query:
            question_ids.append(question.id)
        return question_ids

    # Возвращает текст вопроса
    @staticmethod
    def get_question(question_id):  # Очередной неотвеченный вопрос
        query = Questions.select().where(Questions.id == question_id, Questions.type != 3)
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
            if query[0].type == 0:
                return 0
            elif query[0].type == 1:
                answers = []
                for item in query:
                    answers.append(item.answer)
                return [1, answers]
            elif query[0].type == 2:
                return 2
        else:
            return -1

    # Возвращает текст вопроса и варианты ответа
    @staticmethod
    def get_question_with_answers(question_id):
        question_text = Requests.get_question(question_id)
        if question_text != -1:
            question_answers = Requests.get_question_answers(question_id)
            return [question_text, question_answers]
        else:
            return -1

    # Проверка для следующей функции
    @staticmethod
    def check(user_id, test_id, question_id):
        q1 = Users.select(Users.id).where(Users.id == user_id)
        if len(q1) != 0:
            uid = 1
        else:
            uid = 0
        q2 = Tests.select(Tests.id).where(Tests.id == test_id)
        if len(q2) != 0:
            tid = 1
        else:
            tid = 0
        q3 = Questions.select(Questions.id).where(Questions.id == question_id)
        if len(q3) != 0:
            qid = 1
        else:
            qid = 0
        if uid and tid and qid:
            return 1
        else:
            return 0

    # Запись ответа в таблицу
    @staticmethod
    def write_answer(user_id, test_id, question_id, answer):
        # Проверка, чтобы данные были в БД
        if Requests.check(user_id=user_id, test_id=test_id, question_id=question_id):
            return -1
        query1 = Questions.select(Questions.id, Questions.type).where(Questions.id == question_id, Questions.type != 3)
        if query1[0].type == 0:
            query2 = Answers.select(Answers.id, Answers.question_id, Answers.score).where(
                Answers.question_id == question_id, Answers.type == 0)
            if len(query2) == 0:
                return -1
            if answer == 1:
                answer_id = query2[0].answer_id
                answer_score = query2[0].score
            elif answer == 0:
                answer_id = query2[1].answer_id
                answer_score = query2[1].score
            else:
                return -1
            query3 = UserAnswers(user_id=user_id, test_id=test_id, question_id=question_id, answer_id=answer_id,
                                 score=answer_score)
            query3.save()
            return
        if query1[0].type == 1:
            query2 = Answers.select(Answers.id, Answers.question_id, Answers.score).where(
                Answers.question_id == question_id, Answers.answer == answer, Answers.type == 1)
            if len(query2) == 0:
                return -1
            answer_id = query2[0].answer_id
            answer_score = query2[0].score
            query3 = UserAnswers(user_id=user_id, test_id=test_id, question_id=question_id, answer_id=answer_id,
                                 score=answer_score)
            query3.save()
            return
        if query1[0].type == 2:
            query2 = Answers.select(Answers.id, Answers.question_id, Answers.score).where(
                Answers.question_id == question_id, Answers.type == 2)
            if len(query2) == 0:
                return -1
            answer_id = query2[0].answer_id
            answer_score = 0
            query3 = UserAnswers(user_id=user_id, test_id=test_id, question_id=question_id, answer_id=answer_id,
                                 score=answer_score)
            query3.save()
            return

# Очередной неотвеченный вопрос (номер) и его варианты ответа (лист)
# ПЕРЕДЕЛАТЬ!!!
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
