import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Если токен не найден, выводим сообщение об ошибке
if not BOT_TOKEN:
    print("Ошибка: Переменная окружения BOT_TOKEN не установлена.")
    exit()  # Прерываем работу бота

# Словарь с вопросами и вариантами ответов (callback_data)
questions = {
    1: {
        'text': 'Как часто твой близкий человек употребляет алкоголь или наркотики?',
        'options': [
            {'text': 'Никогда', 'callback_data': '1_0'},
            {'text': 'Редко (1-2 раза в месяц)', 'callback_data': '1_1'},
            {'text': 'Иногда (1-2 раза в неделю)', 'callback_data': '1_2'},
            {'text': 'Часто (почти каждый день)', 'callback_data': '1_3'},
            {'text': 'Очень часто (несколько раз в день)', 'callback_data': '1_4'}
        ]
    },
    2: {
        'text': 'Замечал(а) ли ты, что он/она теряет контроль над количеством употребляемого алкоголя или наркотиков?',
        'options': [
            {'text': 'Да, часто', 'callback_data': '2_2'},
            {'text': 'Да, иногда', 'callback_data': '2_1'},
            {'text': 'Нет, никогда', 'callback_data': '2_0'},
            {'text': 'Затрудняюсь ответить', 'callback_data': '2_1'}
        ]
    },
    3: {
         'text': 'Нужно ли ему/ей больше алкоголя или наркотиков для достижения прежнего эффекта?',
         'options': [
            {'text': 'Да', 'callback_data': '3_2'},
            {'text': 'Нет', 'callback_data': '3_0'},
            {'text': 'Не знаю', 'callback_data': '3_1'}
         ]
    },
    4: {
        'text': 'Бывают ли у него/нее симптомы отмены (ломка, похмелье, раздражительность) при отсутствии алкоголя или наркотиков?',
        'options': [
            {'text': 'Да', 'callback_data': '4_2'},
            {'text': 'Нет', 'callback_data': '4_0'},
            {'text': 'Не знаю', 'callback_data': '4_1'}
        ]
    },
    5: {
        'text': 'Пробовал(а) ли он/она бросить употреблять, но не смог(ла)?',
        'options': [
            {'text': 'Да, несколько раз', 'callback_data': '5_3'},
            {'text': 'Да, один раз', 'callback_data': '5_2'},
            {'text': 'Нет, не пробовал(а)', 'callback_data': '5_0'},
            {'text': 'Не знаю', 'callback_data': '5_1'}
        ]
    },
    6: {
        'text': 'Влияет ли употребление на его/ее работу или учебу?',
        'options': [
            {'text': 'Да, часто пропускает работу/учебу или плохо выполняет свои обязанности', 'callback_data': '6_3'},
            {'text': 'Да, иногда', 'callback_data': '6_2'},
            {'text': 'Нет, не влияет', 'callback_data': '6_0'},
            {'text': 'Не работает/Не учится', 'callback_data': '6_1'}
        ]
    },
    7: {
        'text': 'Изменился ли круг его/ее общения? Появились ли новые друзья, которых ты не знаешь?',
        'options': [
            {'text': 'Да, сильно изменился', 'callback_data': '7_3'},
            {'text': 'Да, немного изменился', 'callback_data': '7_2'},
            {'text': 'Нет, не изменился', 'callback_data': '7_0'},
            {'text': 'Не знаю', 'callback_data': '7_1'}
        ]
    },
    8: {
        'text': 'Стал(а) ли он/она более скрытным/скрытной, лжет ли о своем употреблении?',
        'options': [
            {'text': 'Да, часто', 'callback_data': '8_3'},
            {'text': 'Да, иногда', 'callback_data': '8_2'},
            {'text': 'Нет, не замечал(а)', 'callback_data': '8_0'},
            {'text': 'Не знаю', 'callback_data': '8_1'}
        ]
    },
    9: {
        'text': 'Возникают ли у него/нее финансовые проблемы, связанные с употреблением?',
        'options': [
            {'text': 'Да, постоянно', 'callback_data': '9_3'},
            {'text': 'Да, иногда', 'callback_data': '9_2'},
            {'text': 'Нет, не возникают', 'callback_data': '9_0'},
            {'text': 'Не знаю', 'callback_data': '9_1'}
        ]
    },
    10: {
        'text': 'Страдает ли его/ее здоровье из-за употребления?',
        'options': [
            {'text': 'Да, серьезные проблемы со здоровьем', 'callback_data': '10_3'},
            {'text': 'Да, незначительные проблемы со здоровьем', 'callback_data': '10_2'},
            {'text': 'Нет, не страдает', 'callback_data': '10_0'},
            {'text': 'Не знаю', 'callback_data': '10_1'}
        ]
    },
    11: {
        'text': 'Бывают ли у него/нее перепады настроения, раздражительность, агрессия, связанные с употреблением?',
        'options': [
            {'text': 'Да, часто', 'callback_data': '11_3'},
            {'text': 'Да, иногда', 'callback_data': '11_2'},
            {'text': 'Нет, не замечал(а)', 'callback_data': '11_0'},
            {'text': 'Не знаю', 'callback_data': '11_1'}
        ]
    },
    12: {
        'text': 'Как часто он/она думает об алкоголе или наркотиках?',
        'options': [
            {'text': 'Постоянно', 'callback_data': '12_4'},
            {'text': 'Часто', 'callback_data': '12_3'},
            {'text': 'Иногда', 'callback_data': '12_2'},
            {'text': 'Редко', 'callback_data': '12_1'},
            {'text': 'Никогда', 'callback_data': '12_0'}
        ]
    },
    13: {
        'text': 'Пренебрегает ли он/она своими обязанностями по дому, личной гигиеной из-за употребления?',
        'options': [
            {'text': 'Да, часто', 'callback_data': '13_3'},
            {'text': 'Да, иногда', 'callback_data': '13_2'},
            {'text': 'Нет, не пренебрегает', 'callback_data': '13_0'},
            {'text': 'Не знаю', 'callback_data': '13_1'}
        ]
    },
    14: {
        'text': 'Чувствует ли он/она вину или стыд после употребления?',
        'options': [
            {'text': 'Да, часто', 'callback_data': '14_3'},
            {'text': 'Да, иногда', 'callback_data': '14_2'},
            {'text': 'Нет, не чувствует', 'callback_data': '14_0'},
            {'text': 'Не знаю', 'callback_data': '14_1'}
        ]
    },
    15: {
        'text': 'Происходили ли у него/нее проблемы с законом из-за употребления?',
        'options': [
            {'text': 'Да', 'callback_data': '15_4'},
            {'text': 'Нет', 'callback_data': '15_0'},
            {'text': 'Не знаю', 'callback_data': '15_1'}
        ]
    }
}


def start(update, context: CallbackContext):
    """Обработчик команды /start."""
    context.user_data.clear() # Очищаем данные пользователя, если он уже проходил опрос

    #Приветствие
    update.message.reply_text("Привет! Этот чат-бот поможет тебе оценить, возможно, твоему близкому человеку нужна помощь в связи с употреблением алкоголя или наркотиков. Ответь, пожалуйста, на вопросы максимально честно. Помни, что результаты носят рекомендательный характер и не заменяют консультацию специалиста.")
    send_question(update, context, 1)  # Отправляем первый вопрос

def send_question(update, context: CallbackContext, question_number):
    """Отправляет вопрос с кнопками."""
    question = questions.get(question_number)

    if not question:
        # Если вопросов больше нет, завершаем опрос
        calculate_results(update, context)
        return

    keyboard = []
    for option in question['options']:
        keyboard.append([InlineKeyboardButton(option['text'], callback_data=option['callback_data'])])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query: # Если это ответ на предыдущий вопрос
        update.callback_query.edit_message_text(text=question['text'], reply_markup=reply_markup)
    else: # Если это первый вопрос (после команды /start)
        update.message.reply_text(text=question['text'], reply_markup=reply_markup)

def button(update, context: CallbackContext):
    """Обработчик нажатий на кнопки."""
    query = update.callback_query
    query.answer()  # Отмечаем нажатие кнопки

    # Разбираем callback_data (номер вопроса и балл)
    question_number, score = query.data.split('_')
    # Сохраняем ответ пользователя
    context.user_data[f'question_{question_number}'] = int(score)
    # Отправляем следующий вопрос
    next_question_number = int(question_number) + 1
    send_question(update, context, next_question_number)

def calculate_results(update, context: CallbackContext):
    """Рассчитывает результаты и отправляет рекомендации."""
    total_score = 0
    for i in range(1, 16):
        score = context.user_data.get(f'question_{i}', 0) # Если вопрос не был отвечен, считаем 0
        total_score += score

    if total_score <= 15:
        result_text = "Вероятно, поводов для серьезного беспокойства нет. Однако, стоит продолжать наблюдение за ситуацией."
    elif 16 <= total_score <= 35:
        result_text = "Возможно, есть признаки зависимости. Рекомендуется обратиться к психологу или консультанту по зависимостям для первичной консультации."
    else:
        result_text = "Вероятность зависимости высока. Настоятельно рекомендуется обратиться к специалисту по зависимостям для диагностики и разработки плана лечения."

    final_text = f"Результат: {total_score} балла(ов).\n\n{result_text}\n\nПожалуйста, не стесняйтесь обращаться за помощью! Мы рекомендуем [Название организации/горячей линии помощи зависимым]."
    update.callback_query.edit_message_text(text=final_text) # Используем edit_message_text, чтобы заменить последний вопрос результатами

def main():
    """Запуск бота."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))  # Добавляем обработчик нажатий на кнопки

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
