
class Woman:
    def __init__(self, name, age=40, weight=70):
        self.name = name
        self.age = age
        self.weight = weight
        self.__tits_size = 3

    def get_tits_size(self):
        return self.__tits_size

    def set_tits_size(self, tits_size):
        if tits_size >= 4:
            self.__tits_size = tits_size

class Prostitute(Woman):
    def __init__(self, name, age, weight):
        super().__init__(name, age, weight)
        self.__price = 2000

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

class PornVideos:
    actresses: list()

    def __init__(self, actresses: list):
        self.actresses = actresses

    def add_actresses(self, actresses: list):
        self.actresses = self.actresses + actresses

    def remove_actresses(self, actresses: list):
        for porn_star in actresses:
            if porn_star in self.actresses:
                self.actresses.remove(porn_star)

    def all_actresses_in_video(self):
        for porn_star in self.actresses:
            print(f'Имя: {porn_star.name},', end=" ")
            print(f'Возраст: {porn_star.age},', end=" ")
            print(f'Вес: {porn_star.weight},', end=" ")
            print(f'Цена: {porn_star.get_price()},', end=" ")
            print(f'Размер сисек: {porn_star.get_tits_size()}')
        print()






milf_1 = Woman('Brandi Love', 50, 60)
print(milf_1.name)
print(milf_1.get_tits_size())
milf_1.set_tits_size(5)
print(milf_1.get_tits_size())
print('---------------')

prost_1 = Prostitute('Brandi Love',52, 63)
prost_2 = Prostitute('Ava Adams',51, 75)
prost_3 = Prostitute('Natasha Lux', 43, 95)
prost_3.set_tits_size(10)
prost_3.set_price(1000000)
prost_2.set_price(999999)
porn_video_1 = PornVideos([prost_1, prost_2])
print(porn_video_1.all_actresses_in_video())
print('---------------')
porn_video_1.add_actresses([prost_3])
print(porn_video_1.all_actresses_in_video())
print('---------------')
prost_4 = Prostitute('Madina XXL', 45, 120)
prost_4.set_tits_size(12)
porn_video_1.add_actresses([prost_4])
print(porn_video_1.all_actresses_in_video())


if __name__ == "__main__":
    # Код, который должен выполняться только при прямом запуске Classes.py
    print("Этот код выполняется только при запуске Classes.py напрямую")