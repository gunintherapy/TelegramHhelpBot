import logging
import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ Переменная окружения API_TOKEN не установлена.")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

questions = [
    "1️⃣ Часто ли ваш близкий <b>исчезает без объяснений</b>, отключает телефон и ведёт себя скрытно?",
    "2️⃣ Наблюдаете ли вы <b>резкие перепады настроения</b>, вспышки злости, слёз без повода?",
    "3️⃣ Пропадают ли <b>деньги или вещи</b> из дома? Часто ли он/она просит занять?",
    "4️⃣ Поймали ли вы близкого <b>на лжи</b> больше одного раза?",
    "5️⃣ Сильно ли <b>поменялся круг общения</b>? Появились странные новые друзья?",
    "6️⃣ Есть ли <b>проблемы с работой или учёбой</b>: прогулы, увольнение, конфликты?",
    "7️⃣ Изменилась ли <b>внешность</b>: похудение, мешки под глазами, серый цвет лица?",
    "8️⃣ Есть ли <b>проблемы со сном</b>: бессонница, спит днём, бодрствует ночью?",
    "9️⃣ На ваши опасения отвечает <b>агрессией или отрицанием</b>?",
    "🔟 Чувствуете ли вы <b>усталость, тревогу, бессилие</b> и пытаетесь всё контролировать?"
]

yes_no_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

class TestStates(StatesGroup):
    question = State()

user_data = {}

@dp.message(commands=["start"])
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user_data[message.from_user.id] = {"score": 0, "index": 0}
    await message.answer(
        "👋 Привет! Это чек-лист: <b>«10 признаков, что ваш близкий в зависимости»</b>"


        "Отвечай честно: <b>Да</b> или <b>Нет</b>. Поехали!",
        reply_markup=yes_no_kb
    )
    await state.set_state(TestStates.question)
    await message.answer(questions[0])

@dp.message(TestStates.question)
async def process_question(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = user_data.get(user_id)

    if message.text.lower() == "да":
        data["score"] += 1

    data["index"] += 1

    if data["index"] < len(questions):
        await message.answer(questions[data["index"]])
    else:
           score = data["score"]
    text = f"✅ Вы ответили «да» на {score} из 10 вопросов.\n"



    if score >= 5:
    text += "⚠️ Это серьёзный повод задуматься. Похоже, у вашего близкого может быть зависимость.\n" \
            "Не откладывайте. Помощь есть — напишите специалисту.\n" \
            "<b>📩 Можете написать прямо сюда — поддержка начнётся с первого шага.</b>"
elif 3 <= score < 5:
    text += "🟡 Некоторые признаки есть. Это может быть начальная стадия зависимости или другая сложность.\n" \
            "Будьте внимательны и не бойтесь обратиться за консультацией."
else:
    text += "🟢 Пока что серьёзных признаков нет. Но не теряйте внимательность."

message.reply_text(text, reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")

async def main():
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
