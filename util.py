from bot_requests import Requests
from datetime import datetime
from telebot import types
class Texts:

    @staticmethod
    def bot_info_text():
        text = '''<b>Описание бота</b>\n\nДобро пожаловать в медицинского ассистента! 🤖

Я чат-бот, разработанный для автоматической маршрутизации пациентов к соответствующим специалистам. Ответьте на несколько вопросов, и я помогу определить целевого врача для вашего обращения. <b> Моя цель - обеспечить эффективную направленность к медицинской помощи. </b> Давайте начнем!

Я создан на хакатоне в рамках IV Открытой конференции молодых ученых Центра диагностики и телемедицины (03-04 апреля 2024 г.)'''
        return text

    @staticmethod
    def hello_text():
        text = 'Приветствую! Я - ваш персональный помощник для предварительной маршрутизации вашего визита к врачу. Чтобы максимально эффективно организовать ваше обращение, мне нужно задать несколько вопросов.'
        return text



class Utilities:

    @staticmethod
    def user_age(user):
        b_date = Requests.get_user_b_date(user)
        current_date = datetime.now()
        age = current_date.year - b_date.year - (
                (current_date.month, current_date.day) < (b_date.month, b_date.day))
        return age

    @staticmethod
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
