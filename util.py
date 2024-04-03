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
    def user_sex_and_age(sex, b_date):
        if sex == 'Мужской':
            sex = 'мужчина'
        else:
            sex = 'женщина'
        current_date = datetime.now()
        age = current_date.year - b_date.year - (
                (current_date.month, current_date.day) < (b_date.month, b_date.day))
        if (age % 10 == 1) and (age != 11) and (age != 111):
            return f'{sex} в возрасте {age} года'
        else:
            return f'{sex} в возрасте {age} лет'

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

    @staticmethod
    def calculate_bmi(weight, height):
        # Расчет ИМТ
        try:
            bmi = round(float(weight) / (float(height)/100 ** 2), 2)
            bmi_result = f'{bmi}б классификация типа телосложения по ИМТ - '
            if bmi < 16:
                bmi_result += 'выраженная худощавость'
            elif 16 <= bmi < 17:
                bmi_result += 'умеренная худощавость'
            elif 17 <= bmi < 18.5:
                bmi_result += 'лёгкая худощавость'
            elif 18.5 <= bmi < 25:
                bmi_result += 'нормальный вес'
            elif 25 <= bmi < 30:
                bmi_result += 'преожирение'
            elif 30 <= bmi < 35:
                bmi_result += 'ожирение класса I'
            elif 35 <= bmi < 40:
                bmi_result += 'ожирение класса II'
            else:
                bmi_result += 'ожирение класса III'
            return bmi_result
        except ValueError:
            return 0

    @staticmethod
    def patient_result(list_of_specialists):
        text = 'Вам необходимо обратиться к следующим специалистам:\n'
        for specialist in list_of_specialists:
            text += '<b>' + specialist + '</b>' + '\n'
        text += 'Также каждому врачу уже направлена общая информация о Вашем состоянии'
        return text

    @staticmethod
    def doctors_result(user, dictionary):
        name, surname, patronymic, sex, date_of_birth = Requests.get_user_info(user)
#         for doctor in dictionary:
#             text = f'К Вам на прием направлен(а) {surname} {name} {patronymic}, {Utilities.user_sex_and_age(sex, date_of_birth)}, ИМТ - {Utilities.calculate_bmi()}
# Согласно данным из --(наименование ПО)--:'
