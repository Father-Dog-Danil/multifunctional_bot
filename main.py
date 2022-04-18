import telebot
import config
from PIL import Image, ImageDraw
import random
from telebot import types
from time import sleep
import datetime
from func_image import *
from main_func import *

context_users = {}
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
buttons_main_text = ['🧮калькулятор', '🎲рандомайзер', '🐘слон', '☁погода', '🤔вопрос', 'фотошоп?']
buttons_image = [IB('🔄инверсия'), IB('⬛◻ЧБ'), IB('🟫сепия'), IB('🟥красный'), IB('🟧оранжевый'),
                 IB('🟨жёлтый'), IB('🟩зелёный'), IB('🟦синий'), IB('🟪фиолетовый')]
buttons_image_text = ['🔄инверсия', '⬛◻ЧБ', '🟫сепия', '🟥красный', '🟧оранжевый',
                      '🟨жёлтый', '🟩зелёный', '🟦синий', '🟪фиолетовый']
button_exit = types.KeyboardButton('❌закрыть')
list_image_func = [inversion, black_white, sepia, red, orange, yellow, green, blue, purple]
list_text_func = ['''введите без пробелов: первое число, знак действия, второе число.
пример: 1+3; 1-7; 8/2; 2*3
знаки: "+", "-", "/", "*"
чтоб закрыть калькулятор, напишите''',
'''введите два числа через пробел, между которыми будет диапозон.
чтоб закрыть рандомайзер, напишите''',
'''чтоб закрыть игру "слон", напишите''',
'''введите название города. чтобы вернуться в меню, напишите''',
'''задайте вопрос и бот ответит. чтобы вернуться в меню, напишите''',
'''выберите параметр обработки. чтобы вернуться в меню, напишите''']

markup_image.add(*buttons_image, button_exit, row_width=5)
markup_main.add(*buttons_main, row_width=3)
markup_exit.add(button_exit)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'''эй, {message.from_user.username}, жмякай кнопку''', reply_markup=markup_main)


@bot.message_handler(content_types=["text", "photo"])
def chat(message):
    global flag_command, flag_image
    if message.chat.id in context_users:
        flag_command = context_users[message.chat.id]
    else:
        context_users[message.chat.id] = 0
    if message.text == button_exit.text:
        flag_command = 0
        send_welcome(message)
    if flag_command == 0:
        if message.text in buttons_main_text:
            flag_command = buttons_main_text.index(message.text) + 1
            context_users[message.chat.id] = flag_command
            if message.text == buttons_main_text[-1]:
                bot.send_message(message.chat.id, f'''{list_text_func[flag_command - 1]} {button_exit.text}''',
                                 reply_markup=markup_image)
            else:
                bot.send_message(message.chat.id, f'''{list_text_func[flag_command - 1]} {button_exit.text}''',
                                 reply_markup=markup_exit)
    else:
        if flag_command == 1:
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
    context_users[message.chat.id] = flag_command


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
            list_image_func[flag_image - 1](name)
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
        if message.text in buttons_image_text:
            flag_image = buttons_image_text.index(message.text) + 1
            bot.send_message(message.chat.id, f'скиньте фото. чтобы вернуться в меню, напишите "{button_exit.text}"',
                             reply_markup=markup_exit)
        else:
            bot.send_message(message.chat.id, 'такого фильтра у меня нет(',
                             reply_markup=markup_image)


while True:
    try: bot.polling(none_stop=True)
    except Exception as _ex: sleep(15)
