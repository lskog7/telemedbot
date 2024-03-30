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
        q1 = (
            Questions.select()
            .join(
                Answers,
                join_type=JOIN.LEFT_OUTER,
                on=(Answers.question_id == Questions.id),
            )
            .join(
                UserAnswer,
                join_type=JOIN.LEFT_OUTER,
                on=(Answer.id == UserAnswer.answer_id),
            )
            .where(UserAnswer.user == User.get(User.telegram_id == telegram_id))
        )

        q = Question.select().except_(q1)
        if q.count():
            return q[0]

    @staticmethod
    def get_question_answers(question):  # Все варианты ответов на вопрос
        return Answer.select().where(Answer.question == question)

    # Очередной неотвеченный вопрос и его варианты ответа
    @staticmethod
    def get_next_user_question_and_answers(telegram_id):
        question = Requests.get_user_next_question(telegram_id)
        if question:
            text = Question.select().where(Question.id == question)[0].text
            return text, Requests.get_question_answers(question)
        else:
            return 0

    @staticmethod
    def user_has_answer_on_same_question(telegram_id, answer_id):
        user = User.get(User.telegram_id == telegram_id)
        answer = Answer.get(Answer.id == answer_id)
        question = answer.question
        questions = (
            Question.select()
            .join(
                Answer,
                join_type=JOIN.LEFT_OUTER,
                on=(Question.id == Answer.question_id),
            )
            .join(
                UserAnswer,
                join_type=JOIN.LEFT_OUTER,
                on=(Answer.id == UserAnswer.answer_id),
            )
            .where(UserAnswer.user_id == user)
        )
        return question in questions

    # Подсчет баллов для каждого элемента, исходя из ответов пользователя, и запись результата
    @staticmethod
    def calc_user_grade(telegram_id):
        user = User.get(User.telegram_id == telegram_id)
        user_answer_elements = (
            AnswerElement.select()
            .join(
                Answer,
                join_type=JOIN.LEFT_OUTER,
                on=(Answer.id == AnswerElement.answer_id),
            )
            .join(
                UserAnswer,
                join_type=JOIN.LEFT_OUTER,
                on=(Answer.id == UserAnswer.answer_id),
            )
            .where(UserAnswer.user == user)
        )
        result = ""
        for element in Element.select():
            percent = (
                sum(
                    [
                        answer_element.grade
                        for answer_element in user_answer_elements.select().where(
                            AnswerElement.element == element
                        )
                    ]
                )
                / element.max_grade
                * 100
            )
            if percent >= element.edge_grade:
                result += str(element)
        if result == "":
            result, user.result = 100, 100
        else:
            user.result = int(result)
        user.save()
        return result

    @staticmethod
    def custom_answer(result):
        if result == 100:
            q = """Ваши ответы были успешно обработаны
                   В результате тестирования не было выявлено наличие дефицита
                   ‼️ Результат тестирования не является медицинским диагнозом"""
        else:
            elements = ""
            for element in Element.select():
                if element.id in list(map(int, str(result))):
                    elements += element.name + ", "
            q = f"""Ваши ответы были успешно обработаны
                    В результате тестирования было выявлено наличие дефицита {elements[:-2]}
                    Предлагаем вам ознакомиться с рекомендациями, представленным ниже.
                    ‼️ Результат тестирования не является медицинским диагнозом"""
        return q

    @staticmethod
    def custom_tips(chat_id, result):
        if not result == 100:
            photos = []
            for element in Element.select():
                if element.id in list(map(int, str(result))):
                    photos.append(
                        types.InputMediaPhoto(open(f"tips/{element.name}.png", "rb"))
                    )
            bot.send_media_group(chat_id, photos)

    @staticmethod
    def last_result(telegram_id):
        user = User.get(User.telegram_id == telegram_id)
        result = user.result
        if result == 0:
            q = "Ни одного тестирования не было пройдено"
        elif result == 100:
            q = """В результате тестирования не было выявлено наличие дефицита
‼️ Результат тестирования не является медицинским диагнозом"""
        else:
            elements = ""
            for element in Element.select():
                if element.id in list(map(int, str(result))):
                    elements += element.name + ", "
            q = f"""В результате тестирования было выявлено наличие дефицита {elements[:-2]}
‼️ Результат тестирования не является медицинским диагнозом"""
        return q
