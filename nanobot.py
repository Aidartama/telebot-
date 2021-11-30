import telebot
from birdeke import TOKEN
from telebot import types

bot = telebot.TeleBot(TOKEN)
markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row('iphone','samsung')
@bot.message_handler(commands= ['start'] )

def welcome(message):
    sti = open('assets/sticker.webp', 'rb')

    bot.send_sticker(message.chat.id, sti)


    bot.send_message(message.chat.id, 
        'Добро пожаловать на  мой бот ! Я Айдар ) Мой бот служит - ка онлайн магазин'.format(
            message.from_user,bot.get_me()),
        parse_mode='html',reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type=='private':
        if message.text=='samsung':
            markup=types.InlineKeyboardMarkup(row_width=1)
            item1=types.InlineKeyboardButton('samsung s21 ultra')
            item2=types.InlineKeyboardButton('samsung')
            markup.add(item1,item2)
bot.polling(none_stop=True)
           
        