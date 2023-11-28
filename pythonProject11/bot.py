import telebot
from telebot import types
from main import check, check1
import sqlite3

connect = sqlite3.connect('Tg.db')
cursor = connect.cursor()
connect2 = sqlite3.connect('users.db')
cur = connect2.cursor()

bot = telebot.TeleBot('6423289306:AAGvPkTA5ylEh1M6-ptRUR-1js0hTcScZHQ')


@bot.message_handler(commands=['start'])
def start(message):
    m = types.InlineKeyboardMarkup()
    m1 = types.InlineKeyboardButton(text='Окь, го регаться', callback_data='reg')
    m.add(m1)

    bot.send_message(message.from_user.id, 'Зарегайся по кнопке ниже', reply_markup=m)


@bot.callback_query_handler(lambda call: call.data == 'reg')
def reg(message):
    msg = bot.send_message(message.from_user.id, 'Отправь ответным сообщением логин и пароль, через двоеточие')
    bot.register_next_step_handler(msg, log)


def log(message):
    login, password = message.text.split(';')  # тут надо более точную проверку сделать
    ans = check(login, password)
    print(ans)
    if len(ans) == 0:
        bot.reply_to(message, 'Не нашел такого юзера. Начни заново /start')
        return
    check1(login, password, message.from_user.id)
    bot.reply_to(message, 'Зарегал')


def send_result(chatid, res):
    bot.send_message(chatid, res)


bot.polling()
