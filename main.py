import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

token = '5370441409:AAFn8UtGHOu9F20BJsxtHuJAwNSsMU1tT0A'
bot1 = telebot.TeleBot(token)

headers ={
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}


def make_kb():
    btn1 = types.InlineKeyboardButton("Moscow", callback_data='moscow')
    btn2 = types.InlineKeyboardButton("Tokio", callback_data='tokio')
    btn3 = types.InlineKeyboardButton("New-York", callback_data='new-york')
    btn4 = types.InlineKeyboardButton("London", callback_data='london')
    btn5 = types.InlineKeyboardButton("Berlin", callback_data='berlin')
    row1 = [btn1, btn2, btn3]
    row2 = [btn4, btn5]
    b = [row1, row2]
    mark = types.InlineKeyboardMarkup(b)
    return mark


def make_soup(city_url):
    page = requests.get(city_url, headers=headers)
    return BeautifulSoup(page.content, "html.parser")


def get_img_link(city_url):
    return "https://www.foreca.ru/img/symb-70x70" + make_soup(city_url).find("div", class_="c1").find("img", class_="symb")['src'][15:]


def get_city_name(city_url):
    return make_soup(city_url).find("h1", class_="entry-title").getText()


def get_title(city_url):
    return make_soup(city_url).find("h2", class_="entry-title").getText()


def get_info(city_url):
    return '\n'.join([''.join(a.strip()) for a in make_soup(city_url).find("div", class_="right txt-tight").getText().split('\n')])


def get_weather(city_url):
    return get_city_name(city_url) + " - " + get_title(city_url) + ":" + get_info(city_url)


@bot1.message_handler(commands=['weather'])
def choose_city(message):
    bot1.send_message(message.chat.id, 'Please, choose the city below', reply_markup=make_kb())


@bot1.callback_query_handler(func=lambda call: True)
def which_one(call):
    match call.data:
        case 'moscow':
            bot1.send_photo(call.message.chat.id, get_img_link("https://www.foreca.ru/Russia/Moskva"),
                            caption=get_weather("https://www.foreca.ru/Russia/Moskva"))
            bot1.send_message(call.message.chat.id, 'Please, choose the city below', reply_markup=make_kb())
        case 'tokio':
            bot1.send_photo(call.message.chat.id, get_img_link("https://www.foreca.ru/Japan/Tokyo"),
                            caption=get_weather("https://www.foreca.ru/Japan/Tokyo"))
            bot1.send_message(call.message.chat.id, 'Please, choose the city below', reply_markup=make_kb())
        case 'new-york':
            bot1.send_photo(call.message.chat.id,
                            get_img_link("https://www.foreca.ru/United_States/New_York/New_York_City"),
                            caption=get_weather("https://www.foreca.ru/United_States/New_York/New_York_City"))
            bot1.send_message(call.message.chat.id, 'Please, choose the city below', reply_markup=make_kb())
        case 'london':
            bot1.send_photo(call.message.chat.id, get_img_link("https://www.foreca.ru/United_Kingdom/London"),
                            caption=get_weather("https://www.foreca.ru/United_Kingdom/London"))
            bot1.send_message(call.message.chat.id, 'Please, choose the city below', reply_markup=make_kb())

        case 'berlin':
            bot1.send_photo(call.message.chat.id, get_img_link("https://www.foreca.ru/Germany/Berlin"),
                            caption=get_weather("https://www.foreca.ru/Germany/Berlin"))
            bot1.send_message(call.message.chat.id, 'Please, choose the city below', reply_markup=make_kb())
        case _:
            bot1.send_message(call.message.chat.id, 'Invalid input')


bot1.polling(none_stop=True, interval=0)
