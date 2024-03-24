import telebot
from telebot.types import Message
from telebot import types

from db_model import User, Test, Specialist, Result, Question, Answer, UserAnswer
from peewee import JOIN

bot = telebot.TeleBot('7077776032:AAGJLvl7VZVzmGXDPX6nqIEbetTLSQcuJm8', num_threads=10)


@bot.message_handler(commands=['start', 'menu'])
def registration(message: Message):
    print(message)
    user = message.from_user.id
    if user not in user_list:
        if message.from_user.is_bot is False:
            q = emoji() + 'Привет, Я Минералка - бот, который следит за твоим здоровьем. Тебе не хочется обращаться в больницу, стоять в длинных очередях, сдавать множество анализов и проходить большое количество обследований? Тогда я помогу тебе!'
            bot.send_message(user, text=q)
            bot.send_message(user, text=emoji() + 'Выберите пол', reply_markup=small_keyboard('sex'))
            Requests.write_user(user)
            user_list.append(user)
    else:
        Call.menu(user)

def emoji():
    return '💊‍ '

if __name__ == '__main__':
    print(bot.get_me())
    # bot.set_chat_menu_button()
    command_answers = ['/start', '/menu', '/userinfo', '/botinfo', '/test', '/results', '/help']
    menu_answers = ['/start', '/menu']
    bot_owner = 706803803
    bot.enable_save_next_step_handlers(delay=5)
    bot.load_next_step_handlers()
    bot.polling(none_stop=True)