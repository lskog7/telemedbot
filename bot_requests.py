from db_model import *
from datetime import datetime


# -----------------------------------------------------------------------#
# --------------------------Запросы к данным-----------------------------#
# -----------------------------------------------------------------------#


# -----------------------------Коды ошибок-------------------------------#
# -1 Ошбика запроса, запрос вернул 0 строк
# -2
#
#
#
#
#


# --------------------------Список запросов------------------------------#
class Requests:
    tables_dict = {"00": Qgeneral,
                   "01": Qsurgery,
                   "02": Qcardio,
                   "03": Qdermo,
                   "04": Qendo,
                   "05": Qgastro,
                   "06": Qgyne,
                   "07": Qlor,
                   "08": Qnevro,
                   "09": Qofta,
                   "10": Qpulmo,
                   "11": Qstom,
                   "12": Qsycho,
                   "13": Quro}

    # -------------Проверка на наличение пользователя в БД---------------#
    @staticmethod
    def users_in_db(telegram_id):
        count = Users.select(Users.telegram_id).where(Users.telegram_id == telegram_id).count()
        return count

    # ----------------------Запись пользователя в БД---------------------#
    @staticmethod
    def write_user(telegram_id):
        # Записываем новую строчку в БД
        query = Users(telegram_id=telegram_id, sex=0)
        query.save()

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def get_user_sex(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        return Users.SEX_CHOICES[query[0].sex][1]

    # ----------------------Возвращает имя пользователя------------------#
    @staticmethod
    def get_user_name(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        return query[0].name

    # ----------------------Возвращает фамилию пользователя--------------#
    @staticmethod
    def get_user_surname(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        return query[0].surname

    # ----------------------Возвращает отчество пользователя-------------#
    @staticmethod
    def get_user_patronymic(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        return query[0].patronymic

    # ----------------------Возвращает дату рождения пользователя--------#
    @staticmethod
    def get_user_b_date(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        return query[0].b_date.date()

    # ----------------------Сохраянет имя пользователя-------------------#
    @staticmethod
    def save_user_name(telegram_id, name):
        query = Users.get(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        query.name = name
        query.save()

    # ----------------------Сохраняет фамилию пользователя---------------#
    @staticmethod
    def save_user_surname(telegram_id, surname):
        query = Users.get(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        query.surname = surname
        query.save()

    # ----------------------Сохраняет отчество пользователя--------------#
    @staticmethod
    def save_user_patronymic(telegram_id, patronymic):
        query = Users.get(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        query.patronymic = patronymic
        query.save()

    # ----------------------Сохраняет пол пользователя-------------------#
    @staticmethod
    def save_user_sex(telegram_id, sex):
        query = Users.get(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        query.sex = sex
        query.save()

    # ----------------------Сохраняет доту рождения пользователя---------#
    @staticmethod
    def save_user_b_date(telegram_id, date_str):
        query = Users.get(Users.telegram_id == telegram_id)
        if len(query) == 0:
            return -1
        query.b_date = date_str
        query.save()

    # --------------Возвращает информацию о пользователе----------------#
    # Возвращает список
    @staticmethod
    def get_user_info(telegram_id):
        query = Users.select().where(Users.telegram_id == telegram_id)
        if len(query) != 0:
            user = query[0]
            info = [0 for _ in range(5)]
            info[0] = user.name
            info[1] = user.surname
            info[2] = user.patronymic
            info[3] = Users.SEX_CHOICES[user.sex][1]
            info[4] = user.b_date.date()
            return info
        else:
            return -1

    # -----------------------Начинает тест-------------------------------#
    # ----------------Если есть активный - продолжает его----------------#
    # ----------------Если нет активных - то начинает новый--------------#
    # Возвращает 0 если активных нет и создает новый и номер активного, если он есть
    @staticmethod
    def start_test(telegram_id):
        # Проверяем, есть ли у пользователя активные тесты
        query1 = Users.select().where(Users.telegram_id == telegram_id)  # Должно вернуть 1 строчку
        if len(query1) == 0:
            return -1
        user_current_test = query1[0].current_test
        # Если нет активных тестов начинаем новым, делаем запись в таблице tests, возвращаем ноль
        if user_current_test == 0:
            user_id = query1[0].id
            query2 = Tests(user_id=user_id, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), curr_test=0)
            query2.save()
            return 0
        # Если уже есть начатый тест, но возвращаем его номер
        else:
            return user_current_test

    # ----------Возвращает текущий вопрос для данного пользователя--------#
    # Возвращает две переменные: ТЕКСТ_ВОПРОСА, [СПИСКО_ОТВЕТОВ]
    # При возникновении ошибки возвращает -1, -1
    # При окончании теста -5, -5
    @staticmethod
    def get_user_current_question_with_answers(telegram_id):
        # Получаем юзер айди по ТГ айди
        q = Users.select().where(Users.telegram_id == telegram_id)
        if len(q) == 0:
            return -1
        user_id = q[0].id

        # Смотрим какие у пользователя таблицы в списке, какая текущая, какой вопрос сейчас (должна быть одна строка)
        q = Tests.select().where(Tests.user_id == user_id, Tests.status == 0)
        if len(q) == 0 or len(q) > 1:
            return -1, -1
        question_tables_list = q[0].qtables
        current_table_id = q[0].curqtable  # Возвращает string вида "00"
        current_table = Requests.tables_dict[current_table_id]
        current_question = q[0].curq
        num_questions = len(current_table.select())

        # Смотрим на наличие нулей (это значит, что показатели стандартные)
        # Если текущий лист таблиц вопросов это чисто нолик, то мы начинаем общий опрос
        if question_tables_list == 0 and current_question < num_questions:
            table = Qgeneral
            # Тогда просто переходим к вопросам генеральным
            # Получаем текст вопроса
            q = table.Select().where(table.id == current_question)
            question_text = q[0].text
            question_type = q[0].type
            # Выбираем какой у нас тип вопроса
            if question_type == 0:
                return question_text, 0
            elif question_type == 1:
                # Получаем ответы на вопрос
                q4 = Answers.select().where(Answers.qtable == current_table, Answers.qid == current_question)
                ans = []
                for item in q4:
                    ans.append(item.answer)
                return question_text, ans
            elif question_type == 2:
                return question_text, 2
            else:
                return -1, -1

        # Если основной закончился
        elif question_tables_list == 0 and current_question >= num_questions:
            # Смотрим куда у нас направляет пользователя (считаем скор)
            q = Useranswers.select().where(Useranswers.table_id == "qgeneral", Useranswers.score != "0")
            totalway = ""
            for item in q:
                way = str(item.score)
                totalway += way  # Получаем строку вида "01020304"
            tmp_list_of_tmp_lists = []
            for i in range(0, len(totalway) - 1, 2):
                tmp = totalway[i:i + 2]
                tmp_list_of_tmp_lists.append(tmp)
            result = "".join(sorted(set(tmp_list_of_tmp_lists)))
            if len(result) == 0:
                q = Tests.get(user_id=user_id, status=0)
                q.status = 1
                q.save()
                return -5, -5
            # Записываем это значение в таблицу tests
            q = Tests.get(user_id=user_id, status=0)
            # if len(result[2:]) > 0:
            #     q.qtables = result
            # else:
            #     q.qtables = ""
            q.qtables = result
            q.curqtable = result[:2]
            q.save()

            # Заново узнаем номер текущей таблицы
            q = Tests.select().where(Tests.user_id == user_id, Tests.status == 0)
            if len(q) == 0 or len(q) > 1:
                return -1, -1

            current_table_id = q[0].curqtable  # Возвращает string вида "00"
            current_table = Requests.tables_dict[current_table_id]
            current_question = q[0].curq
            num_questions = len(current_table.select())

            # Получаем текст вопроса
            q = current_table.Select().where(current_table.id == current_question)
            question_text = q[0].text
            question_type = q[0].type
            # Выбираем какой у нас тип вопроса
            if question_type == 0:
                return question_text, 0
            elif question_type == 1:
                # Получаем ответы на вопрос
                q4 = Answers.select().where(Answers.qtable == current_table, Answers.qid == current_question)
                ans = []
                for item in q4:
                    ans.append(item.answer)
                return question_text, ans
            elif question_type == 2:
                return question_text, 2
            else:
                return -1, -1

        # Пока не закончились вопросы в доп списке
        elif question_tables_list != 0 and current_question < num_questions:
            q = Tests.select().where(Tests.user_id == user_id, Tests.status == 0)
            if len(q) == 0 or len(q) > 1:
                return -1, -1

            current_table_id = q[0].curqtable  # Возвращает string вида "00"
            current_table = Requests.tables_dict[current_table_id]
            # Тогда просто переходим к вопросам генеральным
            # Получаем текст вопроса
            q = current_table.Select().where(current_table.id == current_question)
            question_text = q[0].text
            question_type = q[0].type
            # Выбираем какой у нас тип вопроса
            if question_type == 0:
                return question_text, 0
            elif question_type == 1:
                # Получаем ответы на вопрос
                q4 = Answers.select().where(Answers.qtable == current_table, Answers.qid == current_question)
                ans = []
                for item in q4:
                    ans.append(item.answer)
                return question_text, ans
            elif question_type == 2:
                return question_text, 2
            else:
                return -1, -1

        # Если закончились вопросы в доп списке
        elif question_tables_list != 0 and current_question >= num_questions:
            # Смотрим куда у нас направляет пользователя (считаем скор)
            q = Tests.select().where(Tests.user_id == user_id, Tests.status == 0)
            if len(q) == 0 or len(q) > 1:
                return -1, -1
            result = q[0].qtables
            if result == "":
                return -5,-5
            q = Tests.get(user_id=user_id, status=0)
            if len(result) > 2:
                q.qtables = result[2:]
            else:
                q.qtables = ""
            q.curqtable = result[:2]
            q.save()

            # Заново узнаем номер текущей таблицы
            q = Tests.select().where(Tests.user_id == user_id, Tests.status == 0)
            if len(q) == 0 or len(q) > 1:
                return -1, -1

            current_table_id = q[0].curqtable  # Возвращает string вида "00"
            current_table = Requests.tables_dict[current_table_id]
            current_question = q[0].curq
            num_questions = len(current_table.select())

            # Получаем текст вопроса
            q = current_table.Select().where(current_table.id == current_question)
            question_text = q[0].text
            question_type = q[0].type
            # Выбираем какой у нас тип вопроса
            if question_type == 0:
                return question_text, 0
            elif question_type == 1:
                # Получаем ответы на вопрос
                q4 = Answers.select().where(Answers.qtable == current_table, Answers.qid == current_question)
                ans = []
                for item in q4:
                    ans.append(item.answer)
                return question_text, ans
            elif question_type == 2:
                return question_text, 2
            else:
                return -1, -1

        # Если все произошло и потом что-то надо
        else:
            return -2, -2


    #--------------------Запись ответа---------------------------#
    @staticmethod
    def write_answer(telegram_id, answer):
        # Мы узнаем, а что за юзер у нас отвечает
        q = Users.select().where(Users.telegram_id == telegram_id)
        if len(q) == 0 or len(q) > 1:
            return -1
        user_id = q[0].user_id
        # Узнаем, в каком тесте сейчас тыкается пользователь

        query1 = Questions.select().where(Questions.id == question_id, Questions.type != 3)
        if len(query1) == 0:
            return -1

        # Обработка вопросов 0 типа
        if query1[0].type == 0:
            query2 = Answers.select(Answers.id, Answers.question_id, Answers.score).where(
                Answers.question_id == question_id, Answers.type == 0)

            if len(query2) == 0:
                return -1

            answer = int(answer)

            if answer == 1:
                answer_id = query2[0].id
                answer_score = query2[0].score

            elif answer == 0:
                answer_id = query2[1].id
                answer_score = query2[1].score

            else:
                return -1

            Requests.save_current_question(telegram_id, question_id + 1)

            query3 = Useranswers(user_id=user_id, test_id=test_id, question_id=question_id, answer_id=answer_id,
                                 score=answer_score)
            query3.save()
            return

        # Обработка вопросов 1 типа
        if query1[0].type == 1:
            answer = int(answer)

            answer_for_first = Requests.get_question_answers(question_id)[answer]

            query2 = Answers.select(Answers.id, Answers.question_id, Answers.score).where(
                Answers.question_id == question_id, Answers.answer == answer_for_first, Answers.type == 1)

            if len(query2) == 0:
                return -1

            answer_id = query2[0].id
            answer_score = query2[0].score
            Requests.save_current_question(telegram_id, question_id + 1)
            query3 = Useranswers(user_id=user_id, test_id=test_id, question_id=question_id, answer_id=answer_id,
                                 score=answer_score)
            query3.save()
            return

        # Обработка вопросов 2 типа
        if query1[0].type == 2:
            query2 = Answers.select().where(
                Answers.question_id == question_id, Answers.type == 2)

            if len(query2) == 0:
                return -1

            answer_id = query2[0].id
            answer_score = 0
            Requests.save_current_question(telegram_id, question_id + 1)
            query3 = Useranswers(user_id=user_id, test_id=test_id, question_id=question_id, answer_id=answer_id,
                                 score=answer_score, free_answer=answer)
            query3.save()
            return


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

    # -----------------Возвращает информацию о специалистах--------------#
    @staticmethod
    def get_specialists_info(specialists_ids):
        specialists_info = []
        for id in specialists_ids:
            query = Specialists.select(Specialists.info).where(Specialists.id == id)
            info = query[0].info
            specialists_info.append(info)
        return specialists_info

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def get_user_specialists(telegram_id, test_num):
        specialists_ids = Requests.get_user_result(telegram_id, test_num)
        specialists_info = Requests.get_specialists_info(specialists_ids)
        return specialists_info

    # ----------------------Возвращает пол пользователя------------------#
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

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def get_question_ids():
        query = Questions.select(Questions.id).where(Questions.type != 3)
        question_ids = []
        for question in query:
            question_ids.append(question.id)
        return question_ids

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def get_question(question_id):  # Очередной неотвеченный вопрос
        query = Questions.select().where(Questions.id == question_id, Questions.type != 3)
        if len(query) != 0:
            text = query[0].text
            return text
        else:
            return -1

    # ----------------------Возвращает пол пользователя------------------#
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
                return answers
            elif query[0].type == 2:
                return 2
        else:
            return -1

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def get_question_with_answers(question_id):
        question_text = Requests.get_question(question_id)
        if question_text != -1:
            question_answers = Requests.get_question_answers(question_id)
            return question_text, question_answers
        else:
            return -1

    # ----------------------Возвращает пол пользователя------------------#
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

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def get_user_id(telegram_id):
        query = Users.select(Users.id).where(Users.telegram_id == telegram_id)
        return query[0].id


    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def save_current_test(telegram_id, test_id):
        query = Users.get(Users.telegram_id == telegram_id)
        query.current_test = test_id
        query.save()

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def save_current_question(telegram_id, question_id):
        query = Users.get(Users.telegram_id == telegram_id)
        query.current_question = question_id
        query.save()

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def get_current_test(telegram_id):
        query = Users.get(Users.telegram_id == telegram_id)
        current_test = query.current_test
        if current_test < 0:
            return -1
        else:
            return current_test

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def get_current_question(telegram_id):
        query = Users.get(Users.telegram_id == telegram_id)
        current_question = query.current_question
        if current_question < 0:
            return -1
        else:
            return current_question

    # ----------------------Возвращает пол пользователя------------------#
    @staticmethod
    def get_current_test_and_question(telegram_id):
        current_test = Requests.get_current_test(telegram_id)
        if current_test == -1:
            return -1
        current_question = Requests.get_current_question(telegram_id)
        if current_question == -1:
            return current_question
        if current_test == 0:
            return 0
        else:
            if current_question == 0:
                return current_test, 0
            else:
                return current_test, current_question
