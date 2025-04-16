from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



# Инициализация бота и диспетчера
bot = Bot(token='')
dp = Dispatcher()

# Машина состояний
class DepositStates(StatesGroup):
    waiting_for_deposit = State()

# Глобальная переменная для депозита
deposit = None

# Клавиатура
startMenu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/start')],
    [KeyboardButton(text='Ввести депозит')],
    [KeyboardButton(text='Поиск вилок')]
], resize_keyboard=True)

# Стартовая команда
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()  # Очищаем состояние пользователя
    await message.answer(
        "Приветствую!\n\n"
        "Я ВилкаБот - инструмент по поиску букмекерских вилок между БК ОлимпБет и БК Бетсити.\n\n"
        "Ориентируйся на вилки от 5-20%, это оптимальный диапазон, всё что ниже - малая прибыль, всё что выше - мусорные вилки, которые живут несколько секунд.\n\n"
        "Дисклеймер: Казино всегда в плюсе.\n\n"
        "Отключи vpn для более быстрого поиска.\n\n"
        "Нажмите \"Ввести депозит\", чтобы я рассчитал суммы ставок на каждое плечо.",
        reply_markup=startMenu
    )

# Хэндлер для команды "Ввести депозит"
@dp.message(F.text == "Ввести депозит")
async def ask_for_deposit(message: Message, state: FSMContext):
    await message.answer("Введи сумму своего депозита в руб(₽):")
    await state.set_state(DepositStates.waiting_for_deposit)  # Устанавливаем состояние ожидания ввода депозита

# Хэндлер для ввода депозита
@dp.message(DepositStates.waiting_for_deposit)
async def handle_deposit(message: Message, state: FSMContext):
    global deposit
    if message.text.isdigit():
        deposit = int(message.text)
        await message.answer(f"Депозит {deposit} руб. обработан. Теперь нажмите кнопку \"Поиск вилок\".", reply_markup=startMenu)
        await state.clear()  # Очищаем состояние после ввода
    else:
        await message.answer("Ошибка: введено некорректное значение. Пожалуйста, введите целое число.")

# Классы парсинга и функция поиска вилок
class ParsingBetCity:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def open_url(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        # Закрываем всплывающие плашки(окна)
        button1 = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "push-confirm__button")))
        button1.click()
        button2 = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button_green")))
        button2.click()
    def parsing_sport_events(self):
        # Парсит События(матчи)
        sport_events = self.driver.find_elements(By.CLASS_NAME, "line-event__name-team")
        sport_event_list_betcity = [element.text.replace("\n", " - ") for element in sport_events]
        return sport_event_list_betcity

    def parsing_coefficients(self):
        # Парсинг всех коэффициентов, поиск элементов с указанным классом
        coefficients = self.driver.find_elements(By.CLASS_NAME, "line-event__main-bets-button")
        coefficients_list_betcity = []
        for element in coefficients:
            try:
                coefficients_list_betcity.append(element.text.strip())
            except Exception:
                # Пропускаем элементы, которые исчезли
                continue
        return coefficients_list_betcity

    def coefficient_total_less(self, coefficients_list):
        # Коэф Тотал Меньше (ТМ) БК БетСити (каждый 9ый из 10и)
        total_less_betcity = coefficients_list[8::10]
        return total_less_betcity

    def coefficient_total_more(self, coefficients_list):
        # Коэф Тотал Больше (ТБ) БК БетСити (каждый 10ый из 10и)
        total_more_betcity = coefficients_list[9::10]
        return total_more_betcity

    def events_and_coefficients(self, sport_event_list, total_less, total_more):
        # Событие + Коэфы ТМ и ТБ соответсвенно БК БетСити
        event_total_coef_betcity = [list(i) for i in zip(sport_event_list, total_less,total_more)]
        return event_total_coef_betcity


class ParsingOlimpBet:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def open_url(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def click_tabs(self):
        elements = self.driver.find_elements(By.CLASS_NAME, "iconArrow--bwAeE")
        # Цикл делает клик по всем элементам списка elements, кроме первого,
        # т.к. первая вкладка 'футбол' на сайте уже развёрнута,
        # Остальные разворачиваем, чтобы затем спарсить сразу все события(матчи)
        for index, element in enumerate(elements[1:], start=1):
            # Клик по элементу
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
        time.sleep(2)

    def parsing_sport_events(self):
        # Парсит События(матчи) БК Олимп
        sport_events = self.driver.find_elements(By.CLASS_NAME, "teams--H6xTz")
        sport_event_list_olimpbet = [element.text.replace("\n - \n", " - ") for element in sport_events]
        return sport_event_list_olimpbet

    def parsing_coefficients(self):
        # Парсинг всех коэффициентов БК Олимп
        # Поиск элементов с указанным классом
        coefficients = self.driver.find_elements(By.CLASS_NAME, "button--NRoUF")
        coefficients_list_olimpbet = []
        for element in coefficients:
            try:
                coefficients_list_olimpbet.append(element.text.strip())
            except Exception:
                # Пропускаем элементы, которые исчезли
                continue
        return coefficients_list_olimpbet

    def coefficient_total_less(self, coefficients_list):
        # Коэф Тотал Меньше (ТМ) БК Олимп(каждый 9ый из 10и)
        total_less_olimpbet = coefficients_list[8::10]
        return total_less_olimpbet

    def coefficient_total_more(self, coefficients_list):
        # Коэф Тотал Больше (ТБ) БК Олимп(каждый 10ый из 10и)
        total_more_olimpbet = coefficients_list[9::10]
        return total_more_olimpbet

    def events_and_coefficients(self, sport_event_list, total_less, total_more):
        # Событие + Коэфы ТМ и ТБ соответсвенно БК Олимп
        event_total_coef_olimpbet = [list(i) for i in zip(sport_event_list, total_less,total_more)]
        return event_total_coef_olimpbet


def find_arbitrage(event_total_coef_betcity, event_total_coef_olimpbet):
    arbitrage_opportunities = []

    for sport_event_list_betcity, total_less_betcity, total_more_betcity in event_total_coef_betcity:
        for sport_event_list_olimpbet, total_less_olimpbet, total_more_olimpbet in event_total_coef_olimpbet:
            if sport_event_list_betcity == sport_event_list_olimpbet:
                try:
                    total_less_betcity = float(total_less_betcity)
                    total_more_betcity = float(total_more_betcity)
                    total_less_olimpbet = float(total_less_olimpbet)
                    total_more_olimpbet = float(total_more_olimpbet)

                    if total_less_betcity == 0 or total_more_betcity == 0 or total_less_olimpbet == 0 or total_more_olimpbet == 0:
                        # print(f"Неудалось считать коэфы. Пропускаем матч {sport_event_list_betcity}.")
                        continue

                    # Проверка на наличие вилки
                    if 1 / total_less_betcity + 1 / total_more_olimpbet < 1:
                        # Процент прибыли вилки
                        profit_percent = (1 - (1 / total_less_betcity + 1 / total_more_olimpbet)) * 100
                        # Расчёт плеч, т е ставок на два исхода
                        shoulder_1 = int(deposit / (1 + total_less_betcity / total_more_olimpbet))
                        shoulder_2 = int(deposit - shoulder_1)
                        # Элемент списка, содержит всю необходимую информацию о вилке: процент прибыли, название матча, на какие кэфы в какую БК ставить, какие суммы, исходя из депозита.
                        arbitrage_opportunities.append((f"Прибыль: {profit_percent:.1f}%\n матч: {sport_event_list_betcity}\n ТБ Олимп: {total_more_olimpbet} - {shoulder_2}руб\n ТМ Бетсити: {total_less_betcity} - {shoulder_1}руб"))

                    # Проверка на наличие вилки
                    if 1 / total_less_olimpbet + 1 / total_more_betcity < 1:
                        # Процент прибыли вилки
                        profit_percent = (1 - (1 / total_less_olimpbet + 1 / total_more_betcity)) * 100
                        # Расчёт плеч, т е ставок на два исхода
                        shoulder_1 = int(deposit / (1 + total_less_olimpbet / total_more_betcity))
                        shoulder_2 = int(deposit - shoulder_1)
                        # Элемент списка, содержит всю необходимую информацию о вилке: процент прибыли, название матча, на какие кэфы в какую БК ставить, какие суммы, исходя из депозита.
                        arbitrage_opportunities.append((f"Прибыль: {profit_percent:.1f}%\n матч: {sport_event_list_betcity}\n ТМ Олимп: {total_less_olimpbet} - {shoulder_1}руб\n ТБ Бетсити: {total_more_betcity} - {shoulder_2}руб"))

                except ValueError:
                    # Пропускаем некорректные коэффициенты
                    continue

                except ZeroDivisionError:
                    # Обработка деления на ноль (на случай, если не сработала проверка)
                    print(f"Деление на ноль в матче {sport_event_list_betcity}. Пропуск.")
                    continue

    return arbitrage_opportunities


# Хэндлер для поиска вилок
@dp.message(F.text == "Поиск вилок")
async def search_arbitrage(message: Message):
    global deposit
    if deposit is None:
        await message.answer("Сначала введите сумму депозита.")
        return

    # await message.answer("Идёт поиск вилок, подождите...")

    found_arbitrage = False  # Флаг для проверки, найдена ли вилка
    retry_interval = 5  # Интервал между попытками (в секундах)

    # deposit = int(input("Введите деп:"))

    while not found_arbitrage:
        try:
            await message.answer("Идёт поиск вилок...")
            await message.answer("Среднее время поиска 2 мин")
            # Parsing BetCity
            parsing_betcity = ParsingBetCity()
            parsing_betcity.open_url("https://betcity.ru/ru/live?events=17517256")
            sport_event_list_betcity = parsing_betcity.parsing_sport_events()
            coefficients_list_betcity = parsing_betcity.parsing_coefficients()
            total_less_betcity = parsing_betcity.coefficient_total_less(coefficients_list_betcity)
            total_more_betcity = parsing_betcity.coefficient_total_more(coefficients_list_betcity)
            event_total_coef_betcity = parsing_betcity.events_and_coefficients(sport_event_list_betcity, total_less_betcity, total_more_betcity)

            # Parsing OlimpBet
            parsing_olimpbet = ParsingOlimpBet()
            parsing_olimpbet.open_url("https://www.olimp.bet/live")
            parsing_olimpbet.click_tabs()
            sport_event_list_olimpbet = parsing_olimpbet.parsing_sport_events()
            coefficients_list_olimpbet = parsing_olimpbet.parsing_coefficients()
            total_less_olimpbet = parsing_olimpbet.coefficient_total_less(coefficients_list_olimpbet)
            total_more_olimpbet = parsing_olimpbet.coefficient_total_more(coefficients_list_olimpbet)
            event_total_coef_olimpbet = parsing_olimpbet.events_and_coefficients(sport_event_list_olimpbet, total_less_olimpbet, total_more_olimpbet)

            # Поиск вилок
            arbitrage_opportunities = find_arbitrage(event_total_coef_betcity, event_total_coef_olimpbet)

            if arbitrage_opportunities:
                await message.answer("Найдены вилки:")
                for opportunity in arbitrage_opportunities:
                    await message.answer(opportunity)
                found_arbitrage = True
            else:
                await message.answer("Вилки не найдены. Повтор через 5 секунд...")
                time.sleep(retry_interval)  # Задержка перед повторным запуском

        except Exception as e:
            await message.answer(f"Неудалось найти вилки.\n Повтор через {retry_interval} секунд...")
            print(f"Ошибка: {e}. Повтор через {retry_interval} секунд...")
            time.sleep(retry_interval)  # Задержка перед повторным запуском


# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


