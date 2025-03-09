

import json
import os

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        pass

    def eat(self):
        pass

    def to_dict(self):
        # конвертирует объект в словарь для JSON
        return {'type': self.__class__.__name__, 'name': self.name, 'age': self.age}
    @classmethod
    def from_dict(cls, data):
    # создает объект Animal из словаря
        subclasses = {'Bird': Bird, 'Mammal': Mammal, 'Reptile': Reptile}
        return subclasses[data['type']] (data['name'], data['age'])

class Bird(Animal):
    def make_sound(self):
        print(f'{self.name } звучание: трель')

class Mammal(Animal):
    def make_sound(self):
        print(f'{self.name } звучание: рык')

class Reptile(Animal):
    def make_sound(self):
        print(f'{self.name } звучание: шипение')

animals = [Bird('соловей', 1), Mammal('лев', 3), Reptile('змея', 4)]

def animal_sound(animals):
    for animal in animals:
        animal.make_sound()

#классы сотрудников

class Employee:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def to_dict(self):
        return {'name': self.name, 'role': self.role}

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['role'])

class ZooKeeper(Employee):
    def feed_animal(self, animal):
        print(f'{self.name} кормит {animal.name}.')
        animal.eat()

class Veterinarian(Employee):
    def heal_animal(self, animal):
        print(f'{self.name} лечит {animal.name}.')

class Zoo:
    def __init__(self):
        self.animals = []
        self.employees = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f'Животное {animal.name} добавлено в зоопарк.')

    def add_employee(self, employee):
        self.employees.append(employee)
        print(f'Сотрудник {employee.name} ({employee.role}) принят на работу.')

    #сохранение информации в файл и возможность загрузки

    def save_to_file(self, filename='zoo_data.json'):
        data = {
            'animals': [animal.to_dict() for animal in self.animals],
            'employees': [employee.to_dict() for employee in self.employees],
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f'Состояние зоопарка сохранено в {filename}.')

    @classmethod
    def load_from_file(cls, filename='zoo_data.json'):
        if not os.path.exists(filename):
            print('Файл сохранения не найден, создан новый зоопарк')
            return cls()
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        zoo = cls()
        zoo.animals = [Animal.from_dict(animal) for animal in data.get('animals', [])]
        zoo.employees = [Employee.from_dict(employee) for employee in data.get('employees', [])]
        print(f'Состояние зоопарка загружено из {filename}.')
        return zoo

    # удаляет сохраненный файл
    @classmethod
    def reset_zoo(cls, filename='zoo_data,json'):
        if os.path.exists(filename):
            os.remove(filename)
        print('Состояние зоопарка сброшено.')

    # основная программа
if __name__ == "__main__":

    Zoo.reset_zoo() # сброс файла перед запуском

    # Создаем новый зоопарк
    zoo = Zoo()

    # Добавляем животных
    zoo.add_animal(Bird("соловей", 1))
    zoo.add_animal(Mammal("лев", 3))
    zoo.add_animal(Reptile("змея", 4))

    # Нанимаем сотрудников
    keeper = ZooKeeper('Иван Петров', 'смотритель')
    vet = Veterinarian('Мария Иванова', 'ветеринар')
    zoo.add_employee(keeper)
    zoo.add_employee(vet)

    # проверка на полиморфизм
    print('\nЗвуки животных в зоопарке:')
    animal_sound(zoo.animals)

    # ветеринар лечит льва
    vet.heal_animal(zoo.animals[1])

    # смотритель кормит соловья
    keeper.feed_animal(zoo.animals[0])

    # Сохраняем состояние
    zoo.save_to_file()
    # загружаем зоопарк снова и проверяем количество объектов
    new_zoo = Zoo.load_from_file()
    print(f"\nВ зоопарке {len(new_zoo.animals)} животных и {len(new_zoo.employees)} сотрудников.")

