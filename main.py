import telebot
import config
from PIL import Image, ImageDraw
import random
from telebot import types
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from time import sleep
import datetime
from func_image import *
from main_func import *

bot = telebot.TeleBot(config.token)
flag_command = 0
flag_image = 0
flag = 1
markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_exit = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_image = types.ReplyKeyboardMarkup(resize_keyboard=True)
IB = types.KeyboardButton
buttons_main = [IB('🧮калькулятор'), IB('🎲рандомайзер'), IB('🐘слон'), IB('☁погода'),
                IB('🤔вопрос'), IB('фотошоп?')]
buttons_image = [IB('инверсия'), IB('ЧБ'), IB('сепия'), IB('красный'), IB('оранжевый'),
                 IB('жёлтый'), IB('зелёный'), IB('синий'), IB('фиолетовый')]
button_exit = types.KeyboardButton('❌закрыть')

markup_image.add(*buttons_image, button_exit, row_width=5)
markup_main.add(*buttons_main, row_width=3)
markup_exit.add(button_exit)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'''эй, {message.from_user.username}, жмякай кнопку''', reply_markup=markup_main)


@bot.message_handler(content_types=["text", "photo"])
def chat(message):
    global flag_command, flag_image
    if message.text == button_exit.text:
        flag_command = 0
        send_welcome(message)
    if flag_command == 0:
        if message.text == buttons_main[0].text:
            flag_command = 1
            bot.send_message(message.chat.id, f'''введите без пробелов: первое число, знак действия, второе число.
пример: 1+3; 1-7; 8/2; 2*3
знаки: "+", "-", "/", "*"
чтоб закрыть калькулятор, напишите "{button_exit.text}"''', reply_markup=markup_exit)
        elif message.text == buttons_main[1].text:
            flag_command = 2
            bot.send_message(message.chat.id, f'''введите два числа через пробел, между которыми будет диапозон.
чтоб закрыть рандомайзер, напишите "{button_exit.text}"''', reply_markup=markup_exit)
        elif message.text == buttons_main[2].text:
            flag_command = 3
            bot.send_message(message.chat.id, f'чтоб закрыть игру "слон", напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        elif message.text == buttons_main[3].text:
            flag_command = 4
            bot.send_message(message.chat.id,
                             f'введите название города. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        elif message.text == buttons_main[4].text:
            flag_command = 5
            bot.send_message(message.chat.id,
                             f'задайте вопрос и бот ответит. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        elif message.text == buttons_main[5].text:
            flag_command = 6
            bot.send_message(message.chat.id,
                             f'выберите параметр обработки. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_image)
        elif message.text != button_exit.text:
            bot.reply_to(message, 'у меня нет таких функций :(')
    elif flag_command == 1:
        bot.reply_to(message, calculator(message.text))
    elif flag_command == 2:
        bot.reply_to(message, randomize(message.text))
    elif flag_command == 3:
        bot.reply_to(message, elephant(message.text))
    elif flag_command == 4:
        bot.reply_to(message, weather(message.text))
    elif flag_command == 5:
        bot.reply_to(message, questions(message.text))
    elif flag_command == 6:
        image_re(message)


def image_re(message):
    global flag_image, flag
    if flag_image:
        if message.content_type == 'photo':
            raw = message.photo[2].file_id
            name = 'data/' + message.from_user.username + '_' + str(datetime.datetime.now().timestamp()) + '.jpg'
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(name, 'wb') as new_file:
                new_file.write(downloaded_file)
            if flag_image == 1:
                inversion(name)
            elif flag_image == 2:
                black_white(name)
            elif flag_image == 3:
                sepia(name)
            elif flag_image == 4:
                red(name)
            elif flag_image == 5:
                orange(name)
            elif flag_image == 6:
                yellow(name)
            elif flag_image == 7:
                green(name)
            elif flag_image == 8:
                blue(name)
            elif flag_image == 9:
                purple(name)
            if flag:
                img = open(name, 'rb')
                bot.send_photo(message.chat.id, img)
                flag_image = 0
                bot.send_message(message.chat.id,
                                 f'выберите параметр обработки. чтобы вернуться в меню, напишите "{button_exit.text}"',
                                 reply_markup=markup_image)

        else:
            bot.send_message(message.chat.id,
                             f'вы ввели не фото. чтобы вернуться в меню, напишите "{button_exit.text}"')
    else:
        if message.text == buttons_image[0].text:
            flag_image = 1
        elif message.text == buttons_image[1].text:
            flag_image = 2
        elif message.text == buttons_image[2].text:
            flag_image = 3
        elif message.text == buttons_image[3].text:
            flag_image = 4
        elif message.text == buttons_image[4].text:
            flag_image = 5
        elif message.text == buttons_image[5].text:
            flag_image = 6
        elif message.text == buttons_image[6].text:
            flag_image = 7
        elif message.text == buttons_image[7].text:
            flag_image = 8
        elif message.text == buttons_image[8].text:
            flag_image = 9
        if flag_image:
            bot.send_message(message.chat.id, f'скиньте фото. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_exit)


while True:
    try: bot.polling(none_stop=True)
    except Exception as _ex: sleep(15)
