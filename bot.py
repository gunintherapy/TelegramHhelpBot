import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("Ошибка: переменная окружения BOT_TOKEN не установлена.")
    exit()

questions = {
    1: {'text': 'Употребляет ли ваш близкий алкоголь или наркотики чаще, чем раньше?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]},
    2: {'text': 'Скрывает ли он/она своё употребление от вас?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]},
    3: {'text': 'Становится ли он/она агрессивным или раздражительным без употребления?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]},
    4: {'text': 'Отрицает ли проблему, даже при очевидных последствиях?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]},
    5: {'text': 'Меняется ли его/её круг общения?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]},
    6: {'text': 'Есть ли финансовые проблемы, связанные с употреблением?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]},
    7: {'text': 'Замечаете ли проблемы с работой/учёбой?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]},
    8: {'text': 'Были ли проблемы с законом из-за употребления?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]},
    9: {'text': 'Бросал(а) ли он/она, но возвращался(ась) к употреблению?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]},
    10: {'text': 'Есть ли проблемы со здоровьем, вызванные употреблением?', 'options': [{'text': 'Да', 'score': 1}, {'text': 'Нет', 'score': 0}]}
}

def start(update: Update, context: CallbackContext):
    context.user_data['score'] = 0
    context.user_data['q'] = 1
    update.message.reply_text(
        "👋 Привет! Это чек-лист: <b>«10 признаков, что ваш близкий в зависимости»</b>\n\n"
        "Отвечайте честно: <b>Да</b> или <b>Нет</b>.\n\nПоехали!",
        parse_mode="HTML"
    )
    send_question(update, context)

def send_question(update: Update, context: CallbackContext):
    q_num = context.user_data['q']
    question = questions.get(q_num)
    if not question:
        show_result(update, context)
        return

    keyboard = [[InlineKeyboardButton(opt['text'], callback_data=str(opt['score']))] for opt in question['options']]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        update.message.reply_text(question['text'], reply_markup=reply_markup)
    else:
        update.callback_query.edit_message_text(question['text'], reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    score = int(query.data)
    context.user_data['score'] += score
    context.user_data['q'] += 1
    send_question(update, context)

def show_result(update: Update, context: CallbackContext):
    total = context.user_data['score']
    if total >= 6:
        text = "⚠️ Серьёзные признаки зависимости. Обратитесь за помощью к специалисту как можно скорее."
    elif 3 <= total < 6:
        text = "🟡 Некоторые признаки есть. Не игнорируйте тревогу, лучше проконсультироваться."
    else:
        text = "🟢 Пока всё в порядке. Но будьте внимательны к изменениям в будущем."
    update.callback_query.edit_message_text(f"Результат: {total} из 10.\n\n{text}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
