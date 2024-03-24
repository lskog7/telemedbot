import telebot
from telebot.types import Message
from telebot import types

from models import Element, Question, Answer, UserAnswer, User, AnswerElement
from peewee import JOIN

bot = telebot.TeleBot('7077776032:AAGJLvl7VZVzmGXDPX6nqIEbetTLSQcuJm8', num_threads=10)


# вызов менюшек
class Call:

    # вызов меню для пользователя
    @staticmethod
    def menu(user):
        menu_keyboard = types.InlineKeyboardMarkup()
        menu_keyboard.add(types.InlineKeyboardButton(text='Пройти тестирование', callback_data='new_test'))
        menu_keyboard.add(types.InlineKeyboardButton(text='Результат тестирования', callback_data='result'))
        menu_keyboard.add(types.InlineKeyboardButton(text='Параметры', callback_data='parameters'))
        menu_keyboard.add(types.InlineKeyboardButton(text='ᐱ', callback_data='roll_up'))
        bot.send_message(user, text=emoji() + 'Выберите действие', reply_markup=menu_keyboard)

    @staticmethod
    def edit_menu(chat_id, message_id):
        menu_keyboard = types.InlineKeyboardMarkup()
        menu_keyboard.add(types.InlineKeyboardButton(text='Пройти тестирование', callback_data='new_test'))
        menu_keyboard.add(types.InlineKeyboardButton(text='Результат тестирования', callback_data='result'))
        menu_keyboard.add(types.InlineKeyboardButton(text='Параметры', callback_data='parameters'))
        menu_keyboard.add(types.InlineKeyboardButton(text='ᐱ', callback_data='roll_up'))
        bot.edit_message_text(emoji() + 'Выберите действие', chat_id, message_id)
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=menu_keyboard)

    @staticmethod
    def parameters(user):
        sex = User.SEX_CHOICES[Requests.user_sex(user)][1]
        age = Requests.user_age(user)
        parameters_keyboard = types.InlineKeyboardMarkup()
        parameters_keyboard.add(types.InlineKeyboardButton(text='Изменить параметры', callback_data='edit_parameters'))
        parameters_keyboard.add(types.InlineKeyboardButton(text='ᐸ', callback_data='come_back'))
        q = emoji() + 'Параметры\nПол: ' + sex + '\nВозраст: ' + str(age) + convert_age(age)
        bot.send_message(user, text=q, reply_markup=parameters_keyboard)

    @staticmethod
    def edit_parameters(user, chat_id, message_id):
        sex = User.SEX_CHOICES[Requests.user_sex(user)][1]
        age = Requests.user_age(user)
        parameters_keyboard = types.InlineKeyboardMarkup()
        parameters_keyboard.add(types.InlineKeyboardButton(text='Изменить параметры', callback_data='edit_parameters'))
        parameters_keyboard.add(types.InlineKeyboardButton(text='ᐸ', callback_data='come_back'))
        q = emoji() + 'Параметры\nПол: ' + sex + '\nВозраст: ' + str(age) + convert_age(age)
        bot.edit_message_text(q, chat_id, message_id)
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=parameters_keyboard)

    @staticmethod
    def new_test():
        new_test_keyboard = types.InlineKeyboardMarkup()
        new_test_keyboard.add(types.InlineKeyboardButton(text='Начать тестирование', callback_data='start_test'))
        new_test_keyboard.add(types.InlineKeyboardButton(text='ᐸ', callback_data='come_back'))
        return new_test_keyboard

    @staticmethod
    def question(question_and_answers, chat_id, message_id):
        question, answers = question_and_answers[0], question_and_answers[1]
        answers_keyboard = types.InlineKeyboardMarkup()
        for i in range(len(answers)):
            answer_id = Answer.select().where(Answer.id == answers[i])[0]
            answers_keyboard.add(types.InlineKeyboardButton(text=answer_id.text, callback_data=str(answers[i])))
        q = emoji() + question
        bot.edit_message_text(q, chat_id, message_id)
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=answers_keyboard)

    @staticmethod
    def result():
        result_keyboard = types.InlineKeyboardMarkup()
        result_keyboard.add(types.InlineKeyboardButton(text='ᐸ', callback_data='come_back'))
        return result_keyboard

    @staticmethod
    def help(user):
        help_keyboard = types.InlineKeyboardMarkup()
        help_keyboard.add(types.InlineKeyboardButton(text='Feedback', callback_data='feedback'))
        help_keyboard.add(types.InlineKeyboardButton(text='О проекте', callback_data='mineralka'))
        help_keyboard.add(types.InlineKeyboardButton(text='ᐱ', callback_data='roll_up'))
        bot.send_message(user, text=emoji() + 'Выберите действие', reply_markup=help_keyboard)

    @staticmethod
    def mineralka(user):
        mineralka_keyboard = types.InlineKeyboardMarkup()
        mineralka_keyboard.add(types.InlineKeyboardButton(text='ᐱ', callback_data='mineralka_roll_up'))
        text = """Я Минералка - бот, который следит за твоим здоровьем. Тебе не хочется обращаться в больницу, стоять в длинных очередях, сдавать кучу анализов и проходить гору обследований? Тогда ты попал по адресу
В этой программе ты сможешь:
 • Пройти тестирование
 • Узнать больше о состоянии своего организма прямо сейчас,не выходя из дома
 • Получить набор анализов,которые необходимо сдать
 • Получить базовые рекомендации по восполнению дефицита элементов
Команды:
 • /menu - Меню
 • /test - Пройти тестирование
 • /parameters - Параметры
 • /mineralka - Справка 
‼️ Результат тестирования не является клиническим диагнозом
        """
        q = emoji() + text
        bot.send_message(user, text=q, reply_markup=mineralka_keyboard)


class Get:

    @staticmethod
    def start_age(message: Message):
        user = message.from_user.id
        age = message.text
        if age in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите возраст ещё раз')
            bot.register_next_step_handler(message, Get.start_age)
        else:
            try:
                age = int(float(age))
            except ValueError:
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите возраст ещё раз')
                bot.register_next_step_handler(message, Get.start_age)
            else:
                if (age < 1) or (age > 150):
                    bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите возраст ещё раз')
                    bot.register_next_step_handler(message, Get.start_age)
                else:
                    Call.menu(user)
                    Requests.save_user_age(user, age)

    @staticmethod
    def parameters_age(message: Message):
        user = message.from_user.id
        age = message.text
        if age in command_answers:
            if age in menu_answers:
                Call.menu(user)
            else:
                commander(message)
        else:
            try:
                age = int(float(age))
            except ValueError:
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите возраст ещё раз')
                bot.register_next_step_handler(message, Get.parameters_age)
            else:
                if (age < 1) or (age > 150):
                    bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите возраст ещё раз')
                    bot.register_next_step_handler(message, Get.parameters_age)
                else:
                    Requests.save_user_age(user, age)
                    bot.send_message(user, emoji() + 'Изменения сохранены')
                    Call.parameters(user)

    @staticmethod
    def feedback(message: Message):
        user = message.from_user.id
        feedback = message.text
        if feedback in command_answers:
            if feedback in menu_answers:
                Call.menu(user)
            else:
                commander(message)
        else:
            bot.send_message(bot_owner, emoji() + 'Отзыв ' + feedback)
            bot.send_message(user, emoji() + 'Спасибо за Ваш отзыв')

    @staticmethod
    def mail(message: Message):
        content = message.content_type
        if content == 'photo':
            caption = message.caption
            if caption is None:
                caption = ''
            photo = message.json.get('photo')[-1].get('file_id')
            for user in user_list:
                bot.send_photo(user, photo, caption=emoji() + caption)
        elif content == 'text':  # photo type
            text = message.text
            for user in user_list:
                bot.send_message(user, emoji() + text)
        else:
            bot.send_message(bot_owner, emoji() + 'Unavailable type')


class Requests:

    @staticmethod
    def write_user(telegram_id):
        users = User.select().where(User.telegram_id == telegram_id)
        if not users.count():
            u = User(telegram_id=telegram_id, age=0, sex=2, result=0)
            u.save()
            return u

    @staticmethod
    def user_age(telegram_id):
        u = User.select().where(User.telegram_id == telegram_id)
        return int(u[0].age)

    @staticmethod
    def user_sex(telegram_id):
        u = User.select().where(User.telegram_id == telegram_id)
        return int(u[0].sex)

    @staticmethod
    def save_user_age(telegram_id, age):
        u = User.get(User.telegram_id == telegram_id)
        u.age = age
        u.save()

    @staticmethod
    def save_user_sex(telegram_id, sex):
        u = User.get(User.telegram_id == telegram_id)
        u.sex = sex
        u.save()

    @staticmethod
    def get_user_next_question(telegram_id):  # Очередной неотвеченный вопрос
        q1 = (Question
              .select()
              .join(Answer, join_type=JOIN.LEFT_OUTER, on=(Answer.question_id == Question.id))
              .join(UserAnswer, join_type=JOIN.LEFT_OUTER, on=(Answer.id == UserAnswer.answer_id))
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
        questions = (Question
                     .select()
                     .join(Answer, join_type=JOIN.LEFT_OUTER, on=(Question.id == Answer.question_id))
                     .join(UserAnswer, join_type=JOIN.LEFT_OUTER, on=(Answer.id == UserAnswer.answer_id))
                     .where(UserAnswer.user_id == user))
        return question in questions

    # Подсчет баллов для каждого элемента, исходя из ответов пользователя, и запись результата
    @staticmethod
    def calc_user_grade(telegram_id):
        user = User.get(User.telegram_id == telegram_id)
        user_answer_elements = (AnswerElement
                                .select().
                                join(Answer, join_type=JOIN.LEFT_OUTER, on=(Answer.id == AnswerElement.answer_id))
                                .join(UserAnswer, join_type=JOIN.LEFT_OUTER, on=(Answer.id == UserAnswer.answer_id))
                                .where(UserAnswer.user == user))
        result = ''
        for element in Element.select():
            percent = sum([answer_element.grade for answer_element in user_answer_elements.select().where(
                AnswerElement.element == element)]) / element.max_grade * 100
            if percent >= element.edge_grade:
                result += str(element)
        if result == '':
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
            elements = ''
            for element in Element.select():
                if element.id in list(map(int, str(result))):
                    elements += element.name + ', '
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
                    photos.append(types.InputMediaPhoto(open(f'tips/{element.name}.png', 'rb')))
            bot.send_media_group(chat_id, photos)

    @staticmethod
    def last_result(telegram_id):
        user = User.get(User.telegram_id == telegram_id)
        result = user.result
        if result == 0:
            q = 'Ни одного тестирования не было пройдено'
        elif result == 100:
            q = """В результате тестирования не было выявлено наличие дефицита
‼️ Результат тестирования не является медицинским диагнозом"""
        else:
            elements = ''
            for element in Element.select():
                if element.id in list(map(int, str(result))):
                    elements += element.name + ', '
            q = f"""В результате тестирования было выявлено наличие дефицита {elements[:-2]}
‼️ Результат тестирования не является медицинским диагнозом"""
        return q


@bot.message_handler(commands=['start', 'menu'])
def registrar(message: Message):
    print(message)
    user = message.from_user.id
    if user not in user_list:
        is_bot = message.from_user.is_bot
        if is_bot is False:
            q = emoji() + 'Привет, Я Минералка - бот, который следит за твоим здоровьем. Тебе не хочется обращаться в больницу, стоять в длинных очередях, сдавать множество анализов и проходить большое количество обследований? Тогда я помогу тебе!'
            bot.send_message(user, text=q)
            bot.send_message(user, text=emoji() + 'Выберите пол', reply_markup=small_keyboard('sex'))
            Requests.write_user(user)
            user_list.append(user)
    else:
        Call.menu(user)


@bot.message_handler(commands=['parameters', 'test', 'mineralka', 'mail'])
def commander(message: Message):
    user = message.from_user.id
    if user in user_list:
        command = message.text[1:]
        if command == 'parameters':
            Call.parameters(user)
        elif command == 'test':
            bot.send_message(user, text=emoji() + 'Выберите действие', reply_markup=Call.new_test())
        elif command == 'mineralka':
            Call.help(user)
        elif user == bot_owner:
            if command == 'mail':
                bot.register_next_step_handler(message, Get.mail)
        else:
            bot.send_message(user, emoji() + 'OK')
    else:
        is_bot = message.from_user.is_bot
        if is_bot is False:
            bot.send_message(user, emoji() + 'Для входа используйте /start')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == 'roll_up':
        bot.edit_message_reply_markup(chat_id, message_id)
    elif call.data == 'come_back':
        Call.edit_menu(chat_id, message_id)
    elif call.data == 'new_test':
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=Call.new_test())
    elif call.data == 'start_test':
        bot.edit_message_reply_markup(chat_id, message_id)
        Call.question(Requests.get_next_user_question_and_answers(user), chat_id, message_id)
    elif call.data == 'result':
        bot.edit_message_text(Requests.last_result(user), chat_id, message_id)
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=Call.result())
    elif call.data == 'parameters':
        Call.edit_parameters(user, chat_id, message_id)
    elif call.data == 'feedback':
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.send_message(user, emoji() + 'Напишите Ваш отзыв')
        bot.register_next_step_handler(call.message, Get.feedback)
    elif call.data == 'mineralka':
        bot.edit_message_reply_markup(chat_id, message_id)
        Call.mineralka(user)
    elif call.data == 'mineralka_roll_up':
        bot.delete_message(chat_id, message_id)
    elif call.data == 'delete_roll_up':
        bot.delete_message(chat_id, message_id)
        Call.menu(user)
    elif call.data == 'edit_parameters':
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.send_message(user, text=emoji() + 'Выберите пол', reply_markup=small_keyboard('parameters'))
    elif call.data == "sex_male":
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.send_message(user, emoji() + 'Введите возраст')
        Requests.save_user_sex(user, 0)
        bot.register_next_step_handler(call.message, Get.start_age)
    elif call.data == "sex_female":
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.send_message(user, emoji() + 'Введите возраст')
        Requests.save_user_sex(user, 1)
        bot.register_next_step_handler(call.message, Get.start_age)
    elif call.data == 'parameters_male':
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.send_message(user, emoji() + 'Введите возраст')
        Requests.save_user_sex(user, 0)
        bot.register_next_step_handler(call.message, Get.parameters_age)
    elif call.data == 'parameters_female':
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.send_message(user, emoji() + 'Введите возраст')
        Requests.save_user_sex(user, 1)
        bot.register_next_step_handler(call.message, Get.parameters_age)
    else:
        answer_id = int(call.data)
        if not Requests.user_has_answer_on_same_question(user, answer_id):
            user_id = User.get(User.telegram_id == user)
            answer = UserAnswer(user_id=user_id, answer_id=answer_id)
            answer.save()
            question_and_answers = Requests.get_next_user_question_and_answers(user)
            if question_and_answers:
                Call.question(question_and_answers, chat_id, message_id)
            else:
                result = Requests.calc_user_grade(user)
                q = emoji() + Requests.custom_answer(result)
                bot.edit_message_text(q, chat_id, message_id)
                Requests.custom_tips(chat_id, result)
                UserAnswer.delete().where(UserAnswer.user_id == user_id).execute()
        else:
            bot.delete_message(chat_id, message_id)


# emoji в начале любого сообщения
def emoji():
    return '💊‍ '


def convert_age(age):
    int_age = int(age)
    if (int_age % 10 == 1) and (int_age != 11) and (int_age != 111):
        return ' год'
    elif (int_age % 10 > 1) and (int_age % 10 < 5) and (int_age != 12) and (int_age != 13) and (int_age != 14):
        return ' года'
    else:
        return ' лет'


# да или нет кнопки
def small_keyboard(keyboard_type):
    keyboard = types.InlineKeyboardMarkup()
    if keyboard_type == 'sex':  # да или нет для первоначального выбора имени
        keyboard.add(types.InlineKeyboardButton(text='Мужской', callback_data='sex_male'),
                     types.InlineKeyboardButton(text='Женский', callback_data='sex_female'))
    if keyboard_type == 'parameters':  # да или нет для первоначального выбора имени
        keyboard.add(types.InlineKeyboardButton(text='Мужской', callback_data='parameters_male'),
                     types.InlineKeyboardButton(text='Женский', callback_data='parameters_female'))
    return keyboard


if __name__ == '__main__':
    print(bot.get_me())
    # bot.set_chat_menu_button()
    command_answers = ['/start', '/menu', '/parameters', '/test', '/mineralka']
    menu_answers = ['/start', '/menu']
    user_list = [u.telegram_id for u in User.select()]
    bot_owner = 706803803
    UserAnswer.delete().where(UserAnswer.user_id == 1).execute()
    bot.enable_save_next_step_handlers(delay=5)
    bot.load_next_step_handlers()
    bot.polling(none_stop=True)
