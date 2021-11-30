import telebot 
from config import API, TOKEN
from telebot import types
from random import choice, randint 
import requests




bot = telebot.TeleBot(TOKEN)
markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row('Поиск','Инфо',"Рандомное число","Как дела?","Что делаешь?",'Фото')
@bot.message_handler(commands= ['start'] )
def welcome(message):
    sti = open('assets/sticer.webp', 'rb')

    bot.send_sticker(message.chat.id, sti)


    bot.send_message(message.chat.id, 
        'Добро пожаловать пользователь моего бота! \n я'
        '<b>{1.first_name}</b> ваш бот'.format(
            message.from_user,bot.get_me()),
        parse_mode='html',reply_markup=markup
        )
@bot.message_handler(commands=['поиск'])
def welcome(message):
    msg=f'<b>Укажите город:</b>'
    bot.send_message(message.chat.id,msg,parse_mode='html')


@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard=types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    button_geo=types.KeyboardButton(text='Отправь геолокацию',request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id,"Привет!Нажми на кнопку отправь геолокацию",reply_markup=keyboard)


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude:%s"%(message.location.latitude,message.location.longitude))

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type=='private':
        if message.text=='поиск':
            msg=f'<b>Укажите город:</b>'
            bot.send_message(message.chat.id,msg,parse_mode='html')
        elif message.text=='Инфо':
            msg=f'Бот служит для инф и для обшения создатель:мастер'
            bot.send_message(message.chat.id,msg)
        elif message.text=='Рандомное число':
            bot.send_message(message.chat.id,str(randint(0,100)))
        elif message.text=='Что делаешь?':
            spisok_del=['думаю','играю','читаю']
            bot.send_message(message.chat.id, choice(spisok_del))
        elif message.text=='Фото':
            sti = open('inage/xyi.png', 'rb')
            bot.send_photo(message.chat.id,sti)
     
        elif message.text=='Как дела?':
            markup=types.InlineKeyboardMarkup(row_width=2)
            item1=types.InlineKeyboardButton('хорошо',callback_data='good')
            item2=types.InlineKeyboardButton('не очень',callback_data='bad')
            markup.add(item2,item1)
            bot.send_message(message.chat.id,'Отлично,а ты как?',reply_markup=markup)
        else:
            try:
                CITY=message.text
                URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API}"
                response=requests.get(url=URL).json()
                city_info={
                    'city':CITY,
                    'temp':response['main']['temp'],
                    'weather':response['weather'][0]['description'],
                    'wind':response['wind']['speed'],
                    'pressure':response['main']['pressure']
                }
                msg=f"<b><u>{CITY.upper()}</u>\n\nWeather is {city_info['weather']}</b>\n----------------\nTemperature:<b>{city_info['temp']}C</b>\n Wind:<b>{city_info['wind']}m/s</b>\n Pressure:<b>{city_info['pressure']}hPA</b>"
                bot.send_message(message.chat.id,msg,parse_mode='html')
            except:
                msg1=f"<b>Nothing found to country try again:</b>"
                bot.send_message(message.chat.id,msg1,parse_mode='html')
                



@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    try:
        if call.message:
            if call.data=='good':
                bot.send_message(call.message.chat.id,'Вот и отлично!')
            elif call.data=='bad':
                bot.send_message(call.message.chat.id,'Бывает')
            bot.edit_message_text(chat_id=call.message.message_id,text='Как дела?,reply_markup=None')
    except Exception as e:
        print(repr(e))



bot.polling(none_stop=True)