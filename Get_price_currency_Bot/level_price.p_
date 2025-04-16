import requests
import time
from threading import Thread

class SilentMoexPriceAlert:
    def __init__(self):
        # Словарь для хранения всех стоп-уровней {тикер: [список алертов]}
        self.alerts = {}
        # Флаг для контроля работы цикла мониторинга
        self.running = False

    def add_alert(self, ticker, price, direction):
        """Добавляет новый алерт в систему"""
        if ticker not in self.alerts:
            self.alerts[ticker] = []
        self.alerts[ticker].append({
            'price': float(price),       # Целевая цена
            'direction': direction.lower(),  # 'long' или 'short'
            'triggered': False          # Флаг срабатывания
        })

    def check_price(self, ticker):
        """Получает текущую цену акции с MOEX ISS API"""
        url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
        params = {
            "iss.meta": "off",          # Убираем метаданные из ответа
            "securities": ticker,       # Запрашиваем только нужный тикер
            "marketdata.columns": "SECID,LAST"  # Получаем только тикер и цену
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # Проверяем на ошибки HTTP
            data = response.json()
            # Извлекаем данные из поля marketdata -> data
            marketdata = data["marketdata"]["data"]
            # Возвращаем цену, если она есть
            return float(marketdata[0][1]) if marketdata and marketdata[0][1] else None
        except Exception:
            return None  # При ошибке возвращаем None

    def monitor(self, interval=10):
        """Основной цикл мониторинга цен"""
        self.running = True
        print("Мониторинг цен запущен в тихом режиме")

        while self.running:
            try:
                # Проверяем все добавленные тикеры
                for ticker in list(self.alerts.keys()):
                    price = self.check_price(ticker)
                    if price is None:  # Если не получили цену
                        continue      # Пропускаем этот тикер

                    # Проверяем все алерты для этого тикера
                    for alert in self.alerts[ticker]:
                        if alert['triggered']:  # Если алерт уже срабатывал
                            continue           # Пропускаем его

                        # Проверяем условие срабатывания
                        condition_met = (
                            (alert['direction'] == 'long' and price >= alert['price']) or
                            (alert['direction'] == 'short' and price <= alert['price'])
                        )

                        if condition_met:
                            alert['triggered'] = True  # Помечаем как сработавший
                            direction = "выше" if alert['direction'] == 'long' else "ниже"
                            message = (
                                f"🔔 АЛЕРТ! {ticker} достиг {alert['price']} руб. "
                                f"(текущая цена {price} руб., движение {direction} уровня)"
                            )
                            print(message)  # Выводим сообщение о срабатывании

                time.sleep(interval)  # Пауза между проверками
            except Exception:
                time.sleep(60)  # При ошибке делаем большую паузу

    def start_monitoring(self, interval=10):
        """Запускает мониторинг в отдельном потоке"""
        Thread(target=self.monitor, args=(interval,), daemon=True).start()

    def stop_monitoring(self):
        """Останавливает мониторинг"""
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

    print("Мониторинг цен MOEX")
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