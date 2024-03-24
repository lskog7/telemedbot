import telebot
from telebot.types import Message
from telebot import types

from db_model import User, Test, Specialist, Result, Question, Answer, UserAnswer
from peewee import JOIN

bot = telebot.TeleBot('7077776032:AAGJLvl7VZVzmGXDPX6nqIEbetTLSQcuJm8', num_threads=10)





if __name__ == '__main__':
    print(bot.get_me())
    # bot.set_chat_menu_button()
    command_answers = ['/start', '/menu', '/parameters', '/test']
    menu_answers = ['/start', '/menu']
    bot_owner = 706803803
    bot.enable_save_next_step_handlers(delay=5)
    bot.load_next_step_handlers()
    bot.polling(none_stop=True)