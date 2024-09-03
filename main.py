import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time
import threading

bot = telebot.TeleBot("Введите токен")
now = None  # Глобальная переменная для хранения текущего времени

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет! Я чат бот! Я слежу, чтобы ты не забывал(а) принимать таблетку три раза в сутки, в одно и тоже время.')
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()

def send_button_message(chat_id, now):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Я принял(а) таблетку!", callback_data="button_pressed")
    markup.add(button)
    bot.send_message(chat_id, f"Напоминание - прими таблетку! Сейчас {now}.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global now  # Указываем, что используем глобальную переменную
    if call.data == "button_pressed":
        bot.send_message(call.message.chat.id, f"Таблетка была принята в {now}!")

def send_reminders(chat_id):
    global now  # Указываем, что используем глобальную переменную
    first_rem = "07:00"
    second_rem = "15:00"
    end_rem = "23:00"
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == first_rem or now == second_rem or now == end_rem:
            send_button_message(chat_id, now)
            time.sleep(61)
        time.sleep(1)

bot.polling(none_stop=True)


