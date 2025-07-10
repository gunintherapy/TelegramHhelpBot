import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("Ошибка: переменная окружения BOT_TOKEN не установлена.")
    exit()

# Вопросы и варианты ответов
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
        'text': 'Стал(а) ли он/она более скрытным или агрессивным?',
        'options': [
            {'text': 'Да', 'score': 2},
            {'text': 'Нет', 'score': 0},
            {'text': 'Иногда', 'score': 1},
        ]
    },
    4: {
        'text': 'Есть ли проблемы с работой, деньгами или законом?',
        'options': [
            {'text': 'Да', 'score': 2},
            {'text': 'Нет', 'score': 0},
            {'text': 'Иногда', 'score': 1},
        ]
    },
    5: {
        'text': 'Вы часто тревожитесь за этого человека?',
        'options': [
            {'text': 'Почти постоянно', 'score': 3},
            {'text': 'Иногда', 'score': 2},
            {'text': 'Редко', 'score': 1},
            {'text': 'Никогда', 'score': 0},
        ]
    }
}

# Команда /start
def start(update, context: CallbackContext):
    context.user_data['score'] = 0
    context.user_data['q'] = 1
    send_question(update, context)

# Отправка вопроса
def send_question(update, context: CallbackContext):
    q_num = context.user_data['q']
    question = questions.get(q_num)

    if not question:
        show_result(update, context)
        return

    keyboard = [
        [InlineKeyboardButton(opt['text'], callback_data=str(opt['score']))]
        for opt in question['options']
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        update.message.reply_text(question_
