class Currencies:
    __currency: list()

    def __init__(self):
        self.__currency = []

    def add_currency(self, one_curr: str):
        try:
            if type(one_curr) == str:
                self.__currency.append(one_curr)
        except Exception as e:
            print(f'Ошибка: {e}')

    def remove_currency(self, one_curr: str):
        try:
            if type(one_curr) == str:
                if one_curr in self.__currency:
                    self.__currency.remove(one_curr)
        except Exception as e:
            print(f'Ошибка: {e}')

    def get_show_all_currency(self):
        return self.__currency[0] if self.__currency else None

new_curr = Currencies()
new_curr.add_currency('RUB')
print(new_curr.get_show_all_currency())
