import telebot
from telebot.types import Message
from bot_requests import *
from telebot import types
from datetime import datetime
from peewee import JOIN
from sim_crypto import transform_password
from time import sleep

bot = telebot.TeleBot('7077776032:AAGJLvl7VZVzmGXDPX6nqIEbetTLSQcuJm8', num_threads=10)


class Call:

    # вызов меню для пользователя
    @staticmethod
    def menu(user, chat_id=0, message_id=0):
        menu_keyboard = types.InlineKeyboardMarkup()
        menu_keyboard.add(types.InlineKeyboardButton(text='Пройти тестирование', callback_data='new_test'))
        menu_keyboard.add(types.InlineKeyboardButton(text='Результат тестирования', callback_data='result'))
        menu_keyboard.add(types.InlineKeyboardButton(text='Личная информация', callback_data='parameters'))
        menu_keyboard.add(types.InlineKeyboardButton(text='ᐱ', callback_data='roll_up'))
        q = emoji() + 'Выберите действие'
        if chat_id == 0:
            bot.send_message(user, q, reply_markup=menu_keyboard)
        else:
            bot.edit_message_text(q, chat_id, message_id)
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=menu_keyboard)

    @staticmethod
    def edit_parameters(user, chat_id=0, message_id=0):
        name, surname, patronymic, sex, date_of_birth = Requests.get_user_info(user)
        parameters_keyboard = types.InlineKeyboardMarkup()
        parameters_keyboard.add(types.InlineKeyboardButton(text='Изменить ФИО', callback_data='edit_surname'))
        parameters_keyboard.add(types.InlineKeyboardButton(text='Изменить пол', callback_data='edit_sex'))
        parameters_keyboard.add(types.InlineKeyboardButton(text='Изменить дату рождения', callback_data='edit_b_date'))
        parameters_keyboard.add(types.InlineKeyboardButton(text='ᐸ', callback_data='come_back'))
        q = emoji() + f'Личная информация\n<b>ФИО:</b> {surname} {name} {patronymic}\n<b>Пол:</b> {sex}\n<b>Дата рождения:</b> {date_of_birth}'
        if not chat_id:
            bot.send_message(user, text=q, reply_markup=parameters_keyboard, parse_mode='HTML')
        else:
            bot.edit_message_text(q, chat_id, message_id, parse_mode='HTML', reply_markup=parameters_keyboard)
        # bot.edit_message_reply_markup(chat_id, message_id, reply_markup=parameters_keyboard)

    @staticmethod
    def new_test(user, chat_id=0, message_id=0):
        new_test_keyboard = types.InlineKeyboardMarkup()
        new_test_keyboard.add(types.InlineKeyboardButton(text='Начать тестирование', callback_data='start_test'))
        q = emoji() + '<b>Тестирование</b>\n\nКакое-то описать'
        if not chat_id:
            new_test_keyboard.add(types.InlineKeyboardButton(text='ᐱ', callback_data='roll_up'))
            bot.send_message(user, q, parse_mode='HTML', reply_markup=new_test_keyboard)
        else:
            new_test_keyboard.add(types.InlineKeyboardButton(text='ᐸ', callback_data='come_back'))
            bot.edit_message_text(q, chat_id, message_id, parse_mode='HTML', reply_markup=new_test_keyboard)

    @staticmethod
    def question(user, message, chat_id=0, q_type=0):
        message_id = message.message_id
        q_text, q_answers = Requests.get_user_current_question_with_answers(user)
        question_keyboard = types.InlineKeyboardMarkup()
        if q_answers == 0:
            question_keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='yes'),types.InlineKeyboardButton(text='Нет', callback_data='no'))
            if not q_type:
                bot.edit_message_text(q_text, chat_id, message_id, parse_mode='HTML', reply_markup=question_keyboard)
            else:
                bot.send_message(user, q_text, parse_mode='HTML', reply_markup=question_keyboard)
        elif q_answers == 2:
            if not q_type:
                bot.edit_message_text(q_text, chat_id, message_id)
            else:
                bot.send_message(user, q_text, parse_mode='HTML', reply_markup=question_keyboard)
            bot.register_next_step_handler(message, Get.user_answer)
        elif q_answers == -1:
            print(1111)
        else:
            for i in range(len(q_answers)):
                question_keyboard.add(types.InlineKeyboardButton(text=f'{q_answers[i]}', callback_data=f'{i}'))
            if not q_type:
                bot.edit_message_text(q_text, chat_id, message_id, parse_mode='HTML', reply_markup=question_keyboard)
            else:
                bot.send_message(user, q_text, parse_mode='HTML', reply_markup=question_keyboard)

    @staticmethod
    def bot_info(user):
        bot_info_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='ᐱ', callback_data='delete_roll_up'))
        q = emoji() + '''<b>Описание бота</b>\n\nДобро пожаловать в медицинского ассистента! 🤖

Я чат-бот, разработанный для автоматической маршрутизации пациентов к соответствующим специалистам. Ответьте на несколько вопросов, и я помогу определить целевого врача для вашего обращения. <b> Моя цель - обеспечить эффективную направленность к медицинской помощи. </b> Давайте начнем!

Я создан на хакатоне в рамках IV Открытой конференции молодых ученых Центра диагностики и телемедицины (03-04 апреля 2024 г.)'''
        bot.send_message(user, q, parse_mode='HTML', reply_markup=bot_info_keyboard)


class Get:

    @staticmethod
    def start_surname(message: Message):
        user = message.from_user.id
        surname = message.text
        if surname in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите фамилию ещё раз')
            bot.register_next_step_handler(message, Get.start_surname)
        else:
            if surname.isalpha() and len(surname) < 31:
                Requests.save_user_surname(user, surname)
                bot.send_message(user, text=emoji() + f'Введите Ваше имя')
                bot.register_next_step_handler(message, Get.start_name)
            else:
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите фамилию ещё раз')
                bot.register_next_step_handler(message, Get.start_surname)


    @staticmethod
    def start_name(message: Message):
        user = message.from_user.id
        name = message.text
        if name in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите имя ещё раз')
            bot.register_next_step_handler(message, Get.start_name)
        else:
            if name.isalpha() and len(name) < 31:
                Requests.save_user_name(user, name)
                bot.send_message(user, text=emoji() + f'Введите Ваше отчество')
                bot.register_next_step_handler(message, Get.start_patronymic)
            else:
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите имя ещё раз')
                bot.register_next_step_handler(message, Get.start_name)

    @staticmethod
    def start_patronymic(message: Message):
        user = message.from_user.id
        patronymic = message.text
        if patronymic in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите отчество ещё раз')
            bot.register_next_step_handler(message, Get.start_patronymic)
        else:
            if patronymic.isalpha() and len(patronymic) < 31:
                Requests.save_user_patronymic(user, patronymic)
                bot.send_message(user,
                                 text=emoji() + f'Записал ФИО:\n{Requests.get_user_surname(user)} {Requests.get_user_name(user)} {Requests.get_user_patronymic(user)}\n\nВведите дату рождения в формате: ДД.ММ.ГГГГ')
                bot.register_next_step_handler(message, Get.start_age)
            else:
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите отчество ещё раз')
                bot.register_next_step_handler(message, Get.start_patronymic)

    @staticmethod
    def start_age(message: Message):
        user = message.from_user.id
        date_str = message.text
        if date_str in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите дату рождения ещё раз')
            bot.register_next_step_handler(message, Get.start_age)
        else:
            if not all(char.isdigit() or char == '.' for char in date_str):
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите дату рождения ещё раз')
                bot.register_next_step_handler(message, Get.start_age)
            else:
                date_format = "%d.%m.%Y"
                try:
                    date_object = datetime.strptime(date_str, date_format).date()
                    if (date_object.year > 1900) and (date_object <= datetime.now().date()):
                        Requests.save_user_b_date(user, date_object)
                        bot.send_message(user, text=emoji() + f'Записал дату рождения:\n{Requests.get_user_b_date(user)}\n\nВыберите пол:', reply_markup=small_keyboard('sex'))
                    # bot.send_message(user, text=emoji() + 'Выберите пол', reply_markup=small_keyboard('sex'))
                    else:
                        bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите дату рождения ещё раз')
                        bot.register_next_step_handler(message, Get.start_age)
                except ValueError:
                    bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите дату рождения ещё раз')
                    bot.register_next_step_handler(message, Get.start_age)

    @staticmethod
    def edit_surname(message: Message):
        user = message.from_user.id
        surname = message.text
        if surname in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите фамилию ещё раз')
            bot.register_next_step_handler(message, Get.edit_surname)
        else:
            if surname.isalpha() and len(surname) < 31:
                Requests.save_user_surname(user, surname)

                bot.send_message(user, text=emoji() + f'Введите Ваше имя')
                bot.register_next_step_handler(message, Get.edit_name)
            else:
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите фамилию ещё раз')
                bot.register_next_step_handler(message, Get.edit_surname)

    @staticmethod
    def edit_name(message: Message):
        user = message.from_user.id
        name = message.text
        if name in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите имя ещё раз')
            bot.register_next_step_handler(message, Get.edit_name)
        else:
            if name.isalpha() and len(name) < 31:
                Requests.save_user_name(user, name)
                bot.send_message(user, text=emoji() + f'Введите Ваше отчество')
                bot.register_next_step_handler(message, Get.edit_patronymic)
            else:
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите имя ещё раз')
                bot.register_next_step_handler(message, Get.edit_name)

    @staticmethod
    def edit_patronymic(message: Message):
        user = message.from_user.id
        patronymic = message.text
        if patronymic in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите отчество ещё раз')
            bot.register_next_step_handler(message, Get.edit_patronymic)
        else:
            if patronymic.isalpha() and len(patronymic) < 31:
                Requests.save_user_patronymic(user, patronymic)
                Call.edit_parameters(user)
            else:
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите отчество ещё раз')
                bot.register_next_step_handler(message, Get.edit_patronymic)

    @staticmethod
    def edit_age(message: Message):
        user = message.from_user.id
        date_str = message.text
        if date_str in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите дату рождения ещё раз')
            bot.register_next_step_handler(message, Get.edit_age)
        else:
            if not all(char.isdigit() or char == '.' for char in date_str):
                bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите дату рождения ещё раз')
                bot.register_next_step_handler(message, Get.edit_age)
            else:
                date_format = "%d.%m.%Y"
                try:
                    date_object = datetime.strptime(date_str, date_format).date()
                    if (date_object.year > 1900) and (date_object <= datetime.now().date()):
                        Requests.save_user_b_date(user, date_object)
                        Call.edit_parameters(user)
                    else:
                        bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите дату рождения ещё раз')
                        bot.register_next_step_handler(message, Get.edit_age)
                except ValueError:
                    bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите дату рождения ещё раз')
                    bot.register_next_step_handler(message, Get.edit_age)

    @staticmethod
    def user_answer(message: Message):
        user = message.from_user.id

        answer = message.text
        if answer in command_answers:
            bot.send_message(user, emoji() + 'Неверный формат ввода\nВведите дату рождения ещё раз')
            # bot.register_next_step_handler(message, Get.user_answer)
        else:
            try:
                text = float(answer)
                if text > 0:
                    if text == round(text):
                        Requests.write_answer(user, str(int(text)))
                        Call.question(user, message, q_type=1)
                    else:
                        Requests.write_answer(user, str(text))
                        Call.question(user, message, q_type=1)
            except ValueError:
                Requests.write_answer(user, answer)
                Call.question(user, message, q_type=1)



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == 'roll_up':
        bot.edit_message_reply_markup(chat_id, message_id)
    elif call.data == 'come_back':
        Call.menu(user, chat_id, message_id)
    elif call.data == 'new_test':
        Call.new_test(user, chat_id, message_id)
    elif call.data == 'start_test':
        # bot.delete_message(chat_id, message_id)
        if not Requests.get_current_test(user):
            Requests.start_new_test(user)
            Call.question(user, call.message, chat_id)
        else:
            Call.question(user, call.message, chat_id)
    elif call.data == 'result':
        bot.delete_message(chat_id, message_id)
    #     Call.result()
    elif call.data == 'parameters':
        Call.edit_parameters(user, chat_id, call.message)
    elif call.data == 'yes':
        Requests.write_answer(user, 1)
        Call.question(user, call.message, chat_id)
    elif call.data == 'no':
        Requests.write_answer(user, 0)
        Call.question(user, call.message, chat_id)
    # elif call.data == 'feedback':
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     bot.send_message(user, emoji() + 'Напишите Ваш отзыв')
    #     bot.register_next_step_handler(call.message, Get.feedback)
    # elif call.data == 'mineralka':
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     Call.mineralka(user)
    # elif call.data == 'mineralka_roll_up':
    #     bot.delete_message(chat_id, message_id)
    elif call.data == 'delete_roll_up':
        bot.delete_message(chat_id, message_id)
    #     Call.menu(user)
    elif call.data == "sex_male":
        Requests.save_user_sex(user, 1)
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.send_message(user, emoji() + 'Записал:\nПол: Мужской')
        Call.menu(user)
    elif call.data == "sex_female":
        Requests.save_user_sex(user, 2)
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.send_message(user, emoji() + 'Записал:\nПол: Женский')
        Call.menu(user)
    elif call.data == 'edit_surname':
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.edit_message_text(emoji() + 'Введите Вашу фамилию', chat_id, message_id)
        bot.register_next_step_handler(call.message, Get.edit_surname)
    elif call.data == 'edit_sex':
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.edit_message_text(emoji() + 'Выберите пол', chat_id, message_id, reply_markup=small_keyboard('parameters'))
    elif call.data == 'edit_sex_male':
        Requests.save_user_sex(user, 1)
        Call.edit_parameters(user, chat_id, message_id)
    elif call.data == 'edit_sex_female':
        Requests.save_user_sex(user, 2)
        Call.edit_parameters(user, chat_id, message_id)
    elif call.data == 'edit_b_date':
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.edit_message_text(emoji() + 'Введите дату рождения в формате: ДД.ММ.ГГГГ', chat_id, message_id)
        bot.register_next_step_handler(call.message, Get.edit_age)
    else:
        Requests.write_answer(user, int(call.data))
        Call.question(user, call.message, chat_id)



@bot.message_handler(commands=['userinfo', 'botinfo', 'test', 'results', 'help'])
def commander(message: Message):
    user = message.from_user.id
    if Requests.users_in_db(user):
        command = message.text[1:]
        if command == 'userinfo':
            Call.edit_parameters(user)
        elif command == 'test':
            Call.new_test(user)
        elif command == 'results':
            pass
            # Call.result()
        elif command == 'botinfo':
            Call.bot_info(user)
        elif command == 'help':
            pass
        # elif user == bot_owner:
        #     if command == 'mail':
        #         bot.register_next_step_handler(message, Get.mail)
        else:
            bot.send_message(user, emoji() + 'OK')
    else:
        if message.from_user.is_bot is False:
            bot.send_message(user, emoji() + 'Для входа используйте /start')


@bot.message_handler(commands=['start', 'menu'])
def registration(message: Message):
    user = message.from_user.id
    if not Requests.users_in_db(user):
        if message.from_user.is_bot is False:
            q = emoji() + 'Приветствую! Я - ваш персональный помощник для предварительной маршрутизации вашего визита к врачу. Чтобы максимально эффективно организовать ваше обращение, мне нужно задать несколько вопросов.'
            bot.send_message(user, text=q)
            Requests.write_user(user)
            bot.send_message(user, text=emoji() + f'Введите Вашу фамилию')
            bot.register_next_step_handler(message, Get.start_surname)
    else:
        Call.menu(user)


def emoji():
    return '💊‍ '


def small_keyboard(keyboard_type):
    keyboard = types.InlineKeyboardMarkup()
    if keyboard_type == 'name':
        keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='yes_name'),
                     types.InlineKeyboardButton(text='Нет', callback_data='no_name'))
    if keyboard_type == 'sex':
        keyboard.add(types.InlineKeyboardButton(text='Мужской', callback_data='sex_male'),
                     types.InlineKeyboardButton(text='Женский', callback_data='sex_female'))
    if keyboard_type == 'parameters':
        keyboard.add(types.InlineKeyboardButton(text='Мужской', callback_data='edit_sex_male'),
                     types.InlineKeyboardButton(text='Женский', callback_data='edit_sex_female'))
    return keyboard


if __name__ == '__main__':
    print(bot.get_me())
    command_answers = ['/start', '/menu', '/userinfo', '/botinfo', '/test', '/results', '/help']
    menu_answers = ['/start', '/menu']
    bot_owner = 706803803
    Requests.get_user_name(bot_owner)
    bot.enable_save_next_step_handlers(delay=5)
    bot.load_next_step_handlers()
    bot.polling(none_stop=True)
    # bot.infinity_polling()
    # while True:
    #     try:
    #         bot.polling(none_stop=True)
    #     except:
    #         sleep(1)


    # bot.set_chat_menu_button()

