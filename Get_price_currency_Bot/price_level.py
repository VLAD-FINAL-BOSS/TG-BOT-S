# Выводить предупреждение при достижении определенного уровня цены (например, стоп-заявки).

import requests
import time
from datetime import datetime
from threading import Thread
import asyncio


class SilentMoexPriceAlert:
    def __init__(self, bot=None, loop=None):
        self.bot = bot
        self.loop = loop or asyncio.get_event_loop()
        self.alerts = {}
        self.running = False

    def add_alert(self, ticker, price, direction, user_id=0):
        if ticker not in self.alerts:
            self.alerts[ticker] = []

        self.alerts[ticker].append({
            'price': float(price),
            'direction': direction.lower(),
            'triggered': False,
            'user_id': user_id
        })

    def check_price(self, ticker):
        url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
        params = {
            "iss.meta": "off",
            "securities": ticker,
            "marketdata.columns": "SECID,LAST"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            marketdata = data["marketdata"]["data"]
            return float(marketdata[0][1]) if marketdata and marketdata[0][1] else None
        except Exception:
            return None

    async def send_alert(self, user_id, message):
        if self.bot:
            try:
                await self.bot.send_message(user_id, message)
            except Exception as e:
                print(f"[Ошибка отправки]: {e}")
        else:
            print(message)

    def monitor(self, interval=10):
        self.running = True
        print("🔍 Мониторинг цен запущен...")

        while self.running:
            try:
                for ticker in list(self.alerts.keys()):
                    price = self.check_price(ticker)
                    if price is None:
                        continue

                    for alert in self.alerts[ticker]:
                        if alert['triggered']:
                            continue

                        condition_met = (
                            (alert['direction'] == 'long' and price >= alert['price']) or
                            (alert['direction'] == 'short' and price <= alert['price'])
                        )

                        if condition_met:
                            alert['triggered'] = True
                            direction = "выше" if alert['direction'] == 'long' else "ниже"
                            message = (
                                f"🔔 АЛЕРТ! {ticker} достиг {alert['price']} руб. "
                                f"(текущая цена {price} руб., движение {direction} уровня)"
                            )

                            # Корутина отправки сообщения
                            asyncio.run_coroutine_threadsafe(
                                self.send_alert(alert['user_id'], message),
                                self.loop
                            )

                time.sleep(interval)

            except Exception as e:
                print(f"[ERROR]: {e}")
                time.sleep(60)

    def start_monitoring(self, interval=10):
        Thread(target=self.monitor, args=(interval,), daemon=True).start()

    def stop_monitoring(self):
        self.running = False

def setup_alerts(alert_system):
    """Функция для настройки алертов через консоль"""
    print("\nДобавление стоп-уровней (формат: тикер цена long/short)")
    print("Пример: GAZP 160 short - для уведомления при падении ниже 160")
    print("Пример: SBER 300 long - для уведомления при росте выше 300")
    print("Для завершения введите 'q'\n")

    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() == 'q':
                break

            parts = user_input.split()
            if len(parts) != 3:
                print("Неверный формат. Используйте: ТИКЕР ЦЕНА long/short")
                continue

            ticker, price, direction = parts
            if direction.lower() not in ('long', 'short'):
                print("Направление должно быть 'long' или 'short'")
                continue

            alert_system.add_alert(ticker, price, direction)
            print(f"Добавлен алерт: {ticker} {direction} {price}")

        except ValueError:
            print("Ошибка: цена должна быть числом")
        except Exception:
            print("Ошибка ввода")


def main():
    """Основная функция программы"""
    alert_system = SilentMoexPriceAlert()

    print("Тихий мониторинг цен MOEX (без логов)")
    setup_alerts(alert_system)  # Настройка алертов

    if alert_system.alerts:
        alert_system.start_monitoring()  # Запуск мониторинга
        print("\nМониторинг запущен. Работает в фоновом режиме.")
        print("Для выхода нажмите Ctrl+C\n")

        try:
            while True:
                time.sleep(1)  # Бесконечный цикл с минимальной нагрузкой
        except KeyboardInterrupt:
            alert_system.stop_monitoring()
            print("Мониторинг остановлен")
    else:
        print("Не добавлено ни одного алерта")


if __name__ == "__main__":
    main()