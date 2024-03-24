import telebot
from telebot.types import Message
from bot_requests import *
from telebot import types

from db_model import User, Test, Specialist, Result, Question, Answer, UserAnswer
from peewee import JOIN

bot = telebot.TeleBot('7077776032:AAGJLvl7VZVzmGXDPX6nqIEbetTLSQcuJm8', num_threads=10)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == 'roll_up':
        bot.edit_message_reply_markup(chat_id, message_id)
    elif call.data == 'come_back':
        Call.edit_menu(chat_id, message_id)
    elif call.data == 'yes-name':
        bot.send_message(user, text=emoji() + 'Выберите пол', reply_markup=small_keyboard('sex'))
    elif call.data == 'no-name':
        bot.send_message(user, text=emoji() + 'Выберите пол', reply_markup=small_keyboard('sex'))
    # elif call.data == 'new_test':
    #     bot.edit_message_reply_markup(chat_id, message_id, reply_markup=Call.new_test())
    # elif call.data == 'start_test':
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     Call.question(Requests.get_next_user_question_and_answers(user), chat_id, message_id)
    # elif call.data == 'result':
    #     bot.edit_message_text(Requests.last_result(user), chat_id, message_id)
    #     bot.edit_message_reply_markup(chat_id, message_id, reply_markup=Call.result())
    # elif call.data == 'parameters':
    #     Call.edit_parameters(user, chat_id, message_id)
    # elif call.data == 'feedback':
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     bot.send_message(user, emoji() + 'Напишите Ваш отзыв')
    #     bot.register_next_step_handler(call.message, Get.feedback)
    # elif call.data == 'mineralka':
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     Call.mineralka(user)
    # elif call.data == 'mineralka_roll_up':
    #     bot.delete_message(chat_id, message_id)
    # elif call.data == 'delete_roll_up':
    #     bot.delete_message(chat_id, message_id)
    #     Call.menu(user)
    # elif call.data == 'edit_parameters':
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     bot.send_message(user, text=emoji() + 'Выберите пол', reply_markup=small_keyboard('parameters'))
    # elif call.data == "sex_male":
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     bot.send_message(user, emoji() + 'Введите возраст')
    #     Requests.save_user_sex(user, 0)
    #     bot.register_next_step_handler(call.message, Get.start_age)
    # elif call.data == "sex_female":
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     bot.send_message(user, emoji() + 'Введите возраст')
    #     Requests.save_user_sex(user, 1)
    #     bot.register_next_step_handler(call.message, Get.start_age)
    # elif call.data == 'parameters_male':
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     bot.send_message(user, emoji() + 'Введите возраст')
    #     Requests.save_user_sex(user, 0)
    #     bot.register_next_step_handler(call.message, Get.parameters_age)
    # elif call.data == 'parameters_female':
    #     bot.edit_message_reply_markup(chat_id, message_id)
    #     bot.send_message(user, emoji() + 'Введите возраст')
    #     Requests.save_user_sex(user, 1)
    #     bot.register_next_step_handler(call.message, Get.parameters_age)

@bot.message_handler(commands=['start', 'menu'])
def registration(message: Message):
    print(message)
    user = message.from_user.id
    if not Requests.user_in_db(user):
        if message.from_user.is_bot is False:
            q = emoji() + 'Привет'
            bot.send_message(user, text=q)
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            Requests.write_user(user)
            if last_name is not None:
                bot.send_message(user, text=emoji() + f'Вас зовут {last_name} {first_name}?', reply_markup=small_keyboard('name'))
            else:
                bot.send_message(user, text=emoji() + f'Вас зовут {first_name}?', reply_markup=small_keyboard('name'))

    else:
         Call.menu(user)

def emoji():
    return '💊‍ '

def small_keyboard(keyboard_type):
    keyboard = types.InlineKeyboardMarkup()
    if keyboard_type == 'name':
        keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='yes_name'),
                     types.InlineKeyboardButton(text='Нет', callback_data='no_name'))
    # if keyboard_type == 'sex':  # да или нет для первоначального выбора имени
    #     keyboard.add(types.InlineKeyboardButton(text='Мужской', callback_data='sex_male'),
    #                  types.InlineKeyboardButton(text='Женский', callback_data='sex_female'))
    # if keyboard_type == 'parameters':  # да или нет для первоначального выбора имени
    #     keyboard.add(types.InlineKeyboardButton(text='Мужской', callback_data='parameters_male'),
    #                  types.InlineKeyboardButton(text='Женский', callback_data='parameters_female'))
    return keyboard

if __name__ == '__main__':
    print(bot.get_me())
    # bot.set_chat_menu_button()
    command_answers = ['/start', '/menu', '/userinfo', '/botinfo', '/test', '/results', '/help']
    menu_answers = ['/start', '/menu']
    bot_owner = 706803803
    bot.enable_save_next_step_handlers(delay=5)
    bot.load_next_step_handlers()
    bot.polling(none_stop=True)