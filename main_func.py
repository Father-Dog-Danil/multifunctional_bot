import random
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config


flag = 1


def calculator(line):
    flag_calc = 0
    sign = '+'
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
            return int1 + int2
        elif sign == '-':
            return int1 - int2
        elif sign == '/':
            if int2 == 0:
                return 'на ноль делить нельзя, неуч!'
            else:
                if int1 / int2 != int(int1 / int2):
                    return {int1 / int2}
                elif int1 / int2 == int(int1 / int2):
                    return int(int1 / int2)
        elif sign == '*':
            return int1 * int2
    else:
        return 'ты ввёл неправильно, кек'


def questions(text):
    text = text.lower()
    if 'зачем' in text:
        return 'за надом'
    elif 'почему' in text:
        return 'потому что'
    elif 'за что' in text:
        return 'за всё хорошее'
    elif 'кто' in text:
        return 'это я'
    elif 'хочешь' in text:
        return 'не хочу'
    else:
        if random.randint(0, 1):
            return 'да'
        else:
            return 'нет'


def elephant(text):
    return f'все говорят "{text}", а ты купи слона'


def randomize(text):
    text = text.split()
    if len(text) == 2:
        if text[0].isdigit() and text[1].isdigit():
            int1 = int(text[0])
            int2 = int(text[1])
            if int2 < int1:
                return 'почему второе число меньше первого?'
            else:
                return str(random.randint(int1, int2))
        else:
            return 'неправильный формат ввода'
    else:
        return 'почему у тебя не два числа...'


def weather(text):
    api_owm = '015d8c791cd92e4c4094e53aafb81127'
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM(api_owm, config_dict)
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(text)
        degree = observation.weather.temperature('celsius')['temp']
        w = observation.weather.detailed_status
        return f'сейчас в городе {text} {w}, {str(round(degree))} °C'
    except:
        return 'мы не нашли данного места :('
