import telebot
import config
import random
from telebot import types
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from time import sleep

bot = telebot.TeleBot(config.token)
flag_command = 0
markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_exit = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('🧮калькулятор')
button2 = types.KeyboardButton('🎲рандомайзер')
button3 = types.KeyboardButton('🐘слон')
button4 = types.KeyboardButton('☁погода')
button5 = types.KeyboardButton('🤔вопрос')
button6 = types.KeyboardButton('спит')
button_exit = types.KeyboardButton('❌закрыть')
markup_main.add(button1, button2, button3, button4, button5, button6, row_width=3)
markup_exit.add(button_exit)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'''{message.from_user.username}, доброго времени суток, вот список моих команд:
"{button1.text}"
"{button2.text}"
"{button3.text}"
"{button4.text}"
"{button5.text}"''', reply_markup=markup_main)


@bot.message_handler(func=lambda m: True)
def chat(message):
    global flag_command
    if message.text == button_exit.text:
        flag_command = 0
        bot.send_message(message.chat.id,
                         f'''вот список моих команд:
        "{button1.text}"
        "{button2.text}"
        "{button3.text}"
        "{button4.text}"
        "{button5.text}"''', reply_markup=markup_main)
    if flag_command == 0:
        if message.text == button1.text:
            flag_command = 1
            bot.send_message(message.chat.id, f'''введите без пробелов: первое число, знак действия, второе число.
            пример: 1+3
знаки: "+", "-", "/", "*"
чтоб закрыть калькулятор, напишите "{button_exit.text}"''', reply_markup=markup_exit)
        elif message.text == button2.text:
            flag_command = 2
            bot.send_message(message.chat.id, f'''введите два числа через пробел, между которыми будет диапозон.
чтоб закрыть рандомайзер, напишите "{button_exit.text}"''', reply_markup=markup_exit)
        elif message.text == button3.text:
            flag_command = 3
            bot.send_message(message.chat.id, f'чтоб закрыть игру "слон", напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        elif message.text == button4.text:
            flag_command = 4
            bot.send_message(message.chat.id,
                             f'введите название города. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        elif message.text == button5.text:
            flag_command = 5
            bot.send_message(message.chat.id,
                             f'задайте вопрос и бот ответит. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        elif message.text != button_exit.text:
            bot.reply_to(message, 'у меня нет таких функций :(')
    elif flag_command == 1:
        calculator(message)
    elif flag_command == 2:
        randomize(message)
    elif flag_command == 3:
        elephant(message)
    elif flag_command == 4:
        weather(message)
    elif flag_command == 5:
        questions(message)


def questions(message):
    if random.randint(0, 1):
        bot.reply_to(message, f'да')
    else:
        bot.reply_to(message, f'нет')


def elephant(message):
    bot.reply_to(message, f'все говорят "{message.text}", а ты купи слона')


def calculator(message):
    flag_calc = 0
    sign = '+'
    line = message.text
    index = 1
    signs = ['+', '-', '*', '/']
    for i in line:
        if i in signs:
            flag_calc += 1
            sign = i
            index = line.index(i)

    if flag_calc == 1 and line[0:index].isdigit() and line[-1:index:-1].isdigit():
        int1 = int(line[0:index])
        int2 = int(line[index + 1:-1] + line[-1])
        if sign == '+':
            bot.reply_to(message, f'{int1 + int2}')
        elif sign == '-':
            bot.reply_to(message, f'{int1 - int2}')
        elif sign == '/':
            if int2 == 0:
                bot.reply_to(message, 'на ноль делить нельзя, неуч!')
            else:
                if int1 / int2 != int(int1 / int2):
                    bot.reply_to(message, f'{int1 / int2}')
                elif int1 / int2 == int(int1 / int2):
                    bot.reply_to(message, f'{int(int1 / int2)}')
        elif sign == '*':
            bot.reply_to(message, f'{int1 * int2}')
    else:
        bot.reply_to(message, 'ты ввёл неправильно, кек')


def randomize(message):
    text = message.text.split()
    if len(text) == 2:
        if text[0].isdigit() and text[1].isdigit():
            int1 = int(text[0])
            int2 = int(text[1])
            if int2 < int1:
                bot.reply_to(message, 'почему второе число меньше первого?')
            else:
                bot.reply_to(message, str(random.randint(int1, int2)))
        else:
            bot.reply_to(message, 'неправльный формат ввода')
    else:
        bot.reply_to(message, 'почему у тебя не два числа...')


def weather(message):
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM(config.api_owm, config_dict)
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(message.text)
        degree = observation.weather.temperature('celsius')['temp']
        w = observation.weather.detailed_status
        bot.reply_to(message, f'''сейчас в городе {message.text} {w}, {str(round(degree))} °C''')
    except:
        bot.reply_to(message, 'мы не нашли данного места :(')


while True:
        try: bot.polling(none_stop=True)
        except Exception as _ex: sleep(15)
