import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import current_price
from price_level import SilentMoexPriceAlert

# Инициализация системы алертов
alert_system = SilentMoexPriceAlert()
alert_system.start_monitoring()

# Замените на ваш токен
API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Клавиатура с основными командами
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/price"), KeyboardButton(text="/add_alert")],
            [KeyboardButton(text="/my_alerts"), KeyboardButton(text="/help")]
        ],
        resize_keyboard=True
    )


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    welcome_text = """
📈 Привет! Я бот для мониторинга котировок с Московской Биржи.

Основные команды:
/price - Получить текущие котировки
/add_alert - Добавить заявку на уровне (Выводить предупреждение при достижении определенного уровня цены)
/my_alerts - Показать мои текущие заявки
/help - Справка по использованию
    """
    await message.answer(welcome_text, reply_markup=get_main_keyboard())


# Обработчик команды /help
@dp.message(Command("help"))
async def send_help(message: types.Message):
    help_text = """
📌 Как использовать бота:

1. Получение котировок:
   /price - получить цены для инструментов
   (введите тикеры через пробел после команды)

2. Управление алертами:
   /add_alert - добавить новый алерт
   Формат: /add_alert TICKER PRICE DIRECTION
   Пример: /add_alert SBER 300 long
   (direction: long - при росте выше, short - при падении ниже)

   /my_alerts - показать ваши активные алерты
    """
    await message.answer(help_text)


# ✅ Обработка произвольного текстового сообщения
@dp.message()
async def handle_text_message(message: types.Message):
    args = message.text.strip().split()

    # Обработка команды на добавление алерта по шаблону: TICKER PRICE DIRECTION
    if len(args) == 3:
        ticker, price_str, direction = args
        ticker = ticker.upper()
        direction = direction.lower()

        try:
            price = float(price_str)
        except ValueError:
            await message.answer("❗ Цена должна быть числом. Пример: SBER 300 long")
            return

        if direction not in ('long', 'short'):
            await message.answer("❗ Направление должно быть 'long' или 'short'")
            return

        # Добавляем алерт
        alert_system.add_alert(ticker, price, direction)
        direction_text = "выше" if direction == 'long' else "ниже"
        await message.answer(
            f"✅ Алерт добавлен!\n"
            f"Тикер: {ticker}\n"
            f"Цена: {price} руб.\n"
            f"Уведомление при движении {direction_text} указанной цены"
        )
        return

    # Обработка запроса текущих цен: список тикеров
    if all(arg.isalpha() for arg in args):
        tickers = [arg.upper() for arg in args]
        quotes = current_price.get_current_price(tickers)

        if quotes:
            response = "📊 Текущие котировки:\n"
            for ticker, price in quotes.items():
                response += f"{ticker}: {price} руб.\n"
            await message.answer(response)
        else:
            await message.answer("❗ Не удалось получить котировки. Проверьте тикеры.")
        return

    # Если не распознано ни как алерт, ни как тикеры:
    await message.answer("❓ Не распознал сообщение.\n"
                         "Пример для цен: `SBER GAZP`\n"
                         "Пример для алерта: `SBER 300 long`")



# Показ всех алертов пользователя
@dp.message(Command("my_alerts"))
async def show_alerts(message: types.Message):
    if not alert_system.alerts:
        await message.answer("У вас нет активных алертов.")
        return

    response = "📌 Ваши активные алерты:\n\n"
    for ticker, alerts in alert_system.alerts.items():
        for alert in alerts:
            if not alert['triggered']:
                direction = "↑ выше" if alert['direction'] == 'long' else "↓ ниже"
                response += f"{ticker}: {alert['price']} руб. ({direction})\n"

    await message.answer(response if len(response) > 20 else "У вас нет активных алертов.")


# Функция для отправки уведомлений о срабатывании алертов
async def send_alert_notifications():
    while True:
        # Здесь должна быть логика проверки сработавших алертов
        # В вашем случае это уже реализовано в классе SilentMoexPriceAlert
        # и выводится через print(), поэтому нам нужно перехватывать эти сообщения
        # В реальном проекте лучше переделать класс для интеграции с ботом

        # В данном случае просто ждем, так как класс SilentMoexPriceAlert
        # уже самостоятельно обрабатывает алерты и выводит их в консоль
        await asyncio.sleep(10)


# Запуск бота
async def main():
    # Запускаем фоновую задачу для уведомлений
    asyncio.create_task(send_alert_notifications())

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
