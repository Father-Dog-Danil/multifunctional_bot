import telebot
import config
import PIL
from PIL import Image, ImageDraw
import random
from telebot import types
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from time import sleep
import datetime

bot = telebot.TeleBot(config.token)
flag_command = 0
flag_image = 0
markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_exit = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_image = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_main_1 = types.KeyboardButton('🧮калькулятор')
button_main_2 = types.KeyboardButton('🎲рандомайзер')
button_main_3 = types.KeyboardButton('🐘слон')
button_main_4 = types.KeyboardButton('☁погода')
button_main_5 = types.KeyboardButton('🤔вопрос')
button_main_6 = types.KeyboardButton('фотошоп?')

button_image_1 = types.KeyboardButton('инверсия')
button_image_2 = types.KeyboardButton('ЧБ')
button_image_3 = types.KeyboardButton('сепия')

button_exit = types.KeyboardButton('❌закрыть')

markup_image.add(button_image_1, button_image_2, button_image_3, button_exit)

markup_main.add(button_main_1, button_main_2, button_main_3, button_main_4, button_main_5, button_main_6, row_width=3)
markup_exit.add(button_exit)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'''{message.from_user.username}, вот список моих команд:
"{button_main_1.text}"
"{button_main_2.text}"
"{button_main_3.text}"
"{button_main_4.text}"
"{button_main_5.text}"
"{button_main_6.text}"''', reply_markup=markup_main)


@bot.message_handler(content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def chat(message):
    global flag_command
    if message.text == button_exit.text:
        flag_command = 0
        send_welcome(message)
    if flag_command == 0:
        if message.text == button_main_1.text:
            flag_command = 1
            bot.send_message(message.chat.id, f'''введите без пробелов: первое число, знак действия, второе число.
пример: 1+3; 1-7; 8/2; 2*3
знаки: "+", "-", "/", "*"
чтоб закрыть калькулятор, напишите "{button_exit.text}"''', reply_markup=markup_exit)
        elif message.text == button_main_2.text:
            flag_command = 2
            bot.send_message(message.chat.id, f'''введите два числа через пробел, между которыми будет диапозон.
чтоб закрыть рандомайзер, напишите "{button_exit.text}"''', reply_markup=markup_exit)
        elif message.text == button_main_3.text:
            flag_command = 3
            bot.send_message(message.chat.id, f'чтоб закрыть игру "слон", напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        elif message.text == button_main_4.text:
            flag_command = 4
            bot.send_message(message.chat.id,
                             f'введите название города. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        elif message.text == button_main_5.text:
            flag_command = 5
            bot.send_message(message.chat.id,
                             f'задайте вопрос и бот ответит. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        elif message.text == button_main_6.text:
            flag_command = 6
            bot.send_message(message.chat.id,
                             f'выберите параметр обработки. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_image)
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
    elif flag_command == 6:
        image_re(message)


def image_re(message):
    global flag_image
    if flag_image:
        if message.content_type == 'photo':
            raw = message.photo[2].file_id
            name = 'data/' + message.from_user.username + '__' + str(datetime.datetime.now().timestamp()) + '.jpg'
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(name, 'wb') as new_file:
                new_file.write(downloaded_file)
            image = Image.open(name)
            draw = ImageDraw.Draw(image)
            width = image.size[0]
            height = image.size[1]
            pix = image.load()
            if flag_image == 1:
                for x in range(width):
                    for y in range(height):
                        r = pix[x, y][0]
                        g = pix[x, y][1]
                        b = pix[x, y][2]
                        draw.point((x, y), (255 - r, 255 - g, 255 - b))
            if flag_image == 2:
                for x in range(width):
                    for y in range(height):
                        r = pix[x, y][0]
                        g = pix[x, y][1]
                        b = pix[x, y][2]
                        sr = (r + g + b) // 3
                        draw.point((x, y), (sr, sr, sr))
            if flag_image == 3:
                depth = 32
                for x in range(width):
                    for y in range(height):
                        r = pix[x, y][0]
                        g = pix[x, y][1]
                        b = pix[x, y][2]
                        S = (r + g + b) // 3
                        r = S + depth * 2
                        g = S + depth
                        b = S
                        if r > 255:
                            r = 255
                        if b > 255:
                            b = 255
                        if b > 255:
                            b = 255
                        draw.point((x, y), (r, g, b))
            image.save(name)
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
        if message.text == button_image_1.text:
            flag_image = 1
            bot.send_message(message.chat.id, f'введите фото. чтобы вернуться в меню, напишите "{button_exit.text}"')
        elif message.text == button_image_2.text:
            flag_image = 2
            bot.send_message(message.chat.id, f'введите фото. чтобы вернуться в меню, напишите "{button_exit.text}"')
        elif message.text == button_image_3.text:
            flag_image = 3
            bot.send_message(message.chat.id, f'введите фото. чтобы вернуться в меню, напишите "{button_exit.text}"')


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
    if message.text == '1000 - 7' or message.text == '1000-7':
        img = open("data/ken.jpeg", 'rb')
        bot.send_photo(message.chat.id, img, caption='Я умер, прости.')
    else:
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
            bot.reply_to(message, 'неправильный формат ввода')
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
