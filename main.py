import telebot
import webbrowser
from telebot import types
import sqlite3

bot = telebot.TeleBot('7638178693:AAHWMhIW_6Xt5Gp2T5_pQ8fybWqthl_1DlE')
name = None


@bot.message_handler(commands=['start'])
def start(message):
    # markup = types.ReplyKeyboardMarkup()
    # btn1 = types.KeyboardButton("Перейти на сайт")
    # markup.row(btn1)
    #
    # btn2 = types.KeyboardButton("Удалить фото")
    # btn3 = types.KeyboardButton("Изменить текс")
    # markup.row(btn2, btn3)
    #
    # file = open('./red_photo.webp', 'rb')
    # bot.send_photo(message.chat.id, file, reply_markup=markup)
    # # bot.send_audio(message.chat.id, file, reply_markup=markup)
    # bot.send_message(message.chat.id, 'Смотри не удрочись в усмерть 😈', reply_markup=markup)
    #
    # bot.register_next_step_handler(message, on_click)

    # SQL
    conn = sqlite3.connect('mrbotdb.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Введите свое имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('mrbotdb.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, pass) VALUES ("%s", "%s")' % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)

    # bot.register_next_step_handler(message, user_pass)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('mrbotdb.sql')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    info = ''
    for user in users:
        info += f'Имя: {user[1]}, Пароль: {user[2]}\n'

    bot.send_message(call.message.chat.id, info)

    cur.close()
    conn.close()


def on_click(message):
    if message.text.lower() == 'перейти на сайт':
        bot.send_message(message.chat.id, "Website is open")
    elif message.text.lower() == 'удалить фото':
        bot.send_message(message.chat.id, "Deleted")

    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.google.com')


@bot.message_handler(commands=['start', 'main', 'hello'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "<b>Помоги</b> <em>себе</em> сам", parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Перейти на сайт", url='https://google.com')
    markup.row(btn1)

    btn2 = types.InlineKeyboardButton("Удалить фото", callback_data='delete')
    btn3 = types.InlineKeyboardButton("Изменить текс", callback_data='edit')
    markup.row(btn2, btn3)

    bot.reply_to(message, 'Какое красивое фото!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id)


# bot.infinity_polling()
bot.polling(none_stop=True)