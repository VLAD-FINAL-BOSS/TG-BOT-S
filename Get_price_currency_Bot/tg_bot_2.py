import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State

import current_price
from price_level import SilentMoexPriceAlert

# 🔄 FSM Состояния
class BotStates(StatesGroup):
    waiting_for_tickers = State()
    waiting_for_alert = State()



API_TOKEN = '7858545674:AAEYs1HHQprXYhSfTPmL5wnipX1WNu8heHQ'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

alert_system = SilentMoexPriceAlert(bot=bot)  # ← передаём сюда бота
alert_system.start_monitoring()

# 🧩 Клавиатура с командами
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/price"), KeyboardButton(text="/add_alert")],
            [KeyboardButton(text="/my_alerts"), KeyboardButton(text="/help")]
        ],
        resize_keyboard=True
    )


# /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "📈 Привет! Я бот для мониторинга котировок с Московской Биржи.",
        reply_markup=get_main_keyboard()
    )


# /help
@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer(
        "📌 Команды:\n"
        "/price — получить цены (введи тикеры после команды)\n"
        "/add_alert — создать алерт\n"
        "/my_alerts — показать твои алерты"
    )


# /price — начало
@dp.message(Command("price"))
async def price_start(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.waiting_for_tickers)
    await message.answer("🔎 Введите тикеры через пробел (например: SBER GAZP)")


# price — ввод тикеров
@dp.message(BotStates.waiting_for_tickers)
async def get_prices(message: types.Message, state: FSMContext):
    tickers = [t.upper() for t in message.text.strip().split()]
    quotes = current_price.get_current_price(tickers)
    await state.clear()

    if quotes:
        response = "📊 Текущие котировки:\n"
        for ticker, price in quotes.items():
            response += f"{ticker}: {price} руб.\n"
        await message.answer(response)
    else:
        await message.answer("❗ Не удалось получить котировки. Проверьте тикеры.")


# /add_alert — начало
@dp.message(Command("add_alert"))
async def alert_start(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.waiting_for_alert)
    await message.answer("📥 Введите тикер, цену и направление (пример: SBER 300 long)")


# add_alert — ввод параметров
@dp.message(BotStates.waiting_for_alert)
async def process_alert(message: types.Message, state: FSMContext):
    args = message.text.strip().split()
    await state.clear()

    if len(args) != 3:
        await message.answer("❗ Формат: TICKER PRICE DIRECTION\nПример: SBER 300 long")
        return

    ticker, price_str, direction = args
    ticker = ticker.upper()
    direction = direction.lower()

    try:
        price = float(price_str)
    except ValueError:
        await message.answer("❗ Цена должна быть числом.")
        return

    if direction not in ('long', 'short'):
        await message.answer("❗ Направление должно быть 'long' или 'short'")
        return

    # 🧠 Добавляем user_id в alert
    alert_system.add_alert(ticker, price, direction, message.from_user.id)
    dir_text = "выше" if direction == 'long' else "ниже"
    await message.answer(f"✅ Алерт добавлен: {ticker} {price} руб. ({dir_text})")


@dp.message(Command("my_alerts"))
async def show_alerts(message: types.Message):
    user_id = message.from_user.id
    response = "📌 Ваши активные алерты:\n\n"
    has_alerts = False

    for ticker, alerts in alert_system.alerts.items():
        for alert in alerts:
            if not alert['triggered'] and alert['user_id'] == user_id:
                direction = "↑ выше" if alert['direction'] == 'long' else "↓ ниже"
                response += f"{ticker}: {alert['price']} руб. ({direction})\n"
                has_alerts = True

    if has_alerts:
        await message.answer(response)
    else:
        await message.answer("❗ У вас нет активных алертов.")



# ⏰ Псевдо-уведомления (если нужно);;;
async def send_alert_notifications():
    while True:
        # TODO: переделать SilentMoexPriceAlert так, чтобы он отправлял в Telegram по user_id
        await asyncio.sleep(10)


# 🚀 Запуск
async def main():
    asyncio.create_task(send_alert_notifications())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
