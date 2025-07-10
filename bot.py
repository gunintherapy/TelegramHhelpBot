import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("Ошибка: переменная окружения BOT_TOKEN не установлена.")
    exit()

# Список вопросов и вариантов ответа
questions = {
    1: {
        'text': 'Как часто ваш близкий употребляет алкоголь или наркотики?',
        'options': [
            {'text': 'Никогда', 'score': 0},
            {'text': 'Редко', 'score': 1},
            {'text': 'Часто', 'score': 2},
            {'text': 'Почти каждый день', 'score': 3},
        ]
    },
    2: {
        'text': 'Пытался ли он/она бросить, но не смог(ла)?',
        'options': [
            {'text': 'Да', 'score': 2},
            {'text': 'Нет', 'score': 0},
            {'text': 'Не знаю', 'score': 1},
        ]
    },
    3: {
        'text': 'Стал(а) ли он/она б
