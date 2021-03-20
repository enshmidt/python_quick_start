 ## Расширенные возможности

#Декораторы, Итераторы, Генераторы, Дескрипторы

### Декораторы

# Декоратор — функция, которая принимает другую функцию и возвращает функцию обертку

def trace(func):
    def inner(*args, **kwargs):
        print(func.__name__, args, kwargs)
        return func(*args, **kwargs)
    return inner

@trace
def foo(x):
    return 42

foo = trace(foo)

foo(1)

def memoized(func):
    cache = {}
    def inner(x):
        key = x
        if key not in cache:
            print("Calculate new value")
            cache[key] = func(x)
        return cache[key]
    return inner

@memoized
def identity(x):
    "I do nothing useful."
    return x

identity(1)
identity(2)
identity(1)

# Модуль functools.lru_cache

#### Декораторы с аргументами
def trace_arg(handle):
    print("Sart trace_arg")
    def wrapper(func):
        print("Start wrapper")
        def inner(*args, **kwargs):
            print(func.__name__, args, kwargs, file=handle)
            return func(*args, **kwargs)
        return inner
    return wrapper

import sys
@trace_arg(sys.stdout)
def hello(who="body"):
    print("Hi " + who)


hello("me")
hello()


#### Свойства с помощью декоратора
class Decor:
    def __init__(self, value):
        self._data = value

    @classmethod
    def classmethod(cls):
        print("Class: ", cls)

    @staticmethod
    def static():
        print("Hello static")

    @property
    def data(self):
        return self._data + 1

    @data.setter
    def data(self, v):
        self._data = v


d = Decor(3)
d.data
d.classmethod()
d.static()
Decor.static()
d._data
d.data = 2


### Итераторы
# Для унификации работы с последовательностями содзан специальный протокол.
# Объект реализующий этот протокол называется "Итератор"
# Итератор это класс реализующй методы __iter__() и __next__()
# итераторы файлов
# итераторы встроенных типов

import random
class MyRandomIterator():
    def __init__(self, a):
        self.amount = a
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.amount:
            self.counter += 1
            return random.random()
        raise StopIteration



LI = MyRandomIterator(2)
type(LI)
LI.__next__()
LI.__next__()
LI.__next__()

#работа с элементами массива с помощью цикла
for l in MyRandomIterator(4):
    print(l)


### Генераторы

# Генераторное выражение
(i for i in [1,2])

def sequence_gen(n):
    c = 0
    while c < n:
        yield c
        c += 1

b = sequence_gen(4)

type(sequence_gen)
type(b)


for i in sequence_gen(3):
    print(i)

### Генераторы в виде функции
def skip_comments(filename, mode='r', comment='#'):
    print("*** generator is called the first time")
    for line in open(filename, mode):
        if line.startswith(comment):
            continue
        yield line
    print("*** generator is called the last time")


for line in skip_comments("lessons/examples/fox.txt"):
    print(line.strip())

sc = skip_comments("lessons/examples/fox.txt")
sc.__next__()


### Дескрипторы
# Дескриптор — это: экземпляр класса, реализующего протокол дескрипторов
# Функции протокола __get__, __set__, __delete__
class NonNegative:
    def __init__(self, value):
        self.value = value
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        assert value >= 0, "non-negative value required"
        self.value = value
    def __delete__(self, instance):
        self.value = None


class VerySafe:
    x = NonNegative(1)
    y = NonNegative(2)

very_safe = VerySafe()
very_safe.x = 42
very_safe.x
very_safe.x = -42


## Идиоматика Python

# Пиши код, как настоящий Питонист: идиоматика Python

### Проверка истиности для множеств
# if x:
# if not x:
# GOOD
name = 'Safe'
pets = ['Dog', 'Cat', 'Hamster']
owners = {'Safe': 'Cat', 'George': 'Dog'}
if name and pets and owners:
    print('We have pets!')

# NOT SO GOOD
if name != '' and len(pets) > 0 and owners != {}:
    print('We have pets!')

bool({})
bool({1:2})


###  Использовать выражение "in": if x in items
# GOOD
name = 'Safe Hammad'
if 'H' in name:
    print('This name has an H in it!')

# NOT SO GOOD
name = 'Safe Hammad'
if name.find('H') != -1:
    print('This name has an H in it!')

### for x in items
# GOOD
pets = ['Dog', 'Cat', 'Hamster']
for pet in pets:
    print('A', pet, 'can be very cute!')

# NOT SO GOOD
pets = ['Dog', 'Cat', 'Hamster']
i = 0
while i < len(pets):
    print('A', pets[i], 'can be very cute!')
    i += 1

### Обмен значениями двух переменных
a = 1
b = 2
a, b = b, a
print(a, b)

### Объединение списков в строку: ''.join(some_strings)
# GOOD
chars = ['This', 'is', 'the', 'webinar']
name = '\n'.join(chars)
print(name) # Safe

# NOT SO GOOD
chars = ['S', 'a', 'f', 'e']
name = ''
for char in chars:
    name += char
print(name) # Safe

### Использовать enumerate
# for i, item in enumerate(items):
# GOOD
names = ['Safe', 'George', 'Mildred']
for i, name in enumerate(names):
    print(i, name) # 0 Safe, 1 George etc.

# NOT SO GOOD
names = ['Safe', 'George', 'Mildred']
count = 0
for name in names:
    print(i, name) # 0 Safe, 1 George etc.
    count += 1

### Использовать генераторы списков
# GOOD
data = [7, 20, 3, 15, 11]
result = [i * 3 for i in data
          if i > 10]
print(result) # [60, 45, 33]

# NOT SO GOOD (MOST OF THE TIME)
data = [7, 20, 3, 15, 11]
result = []
for i in data:
    if i > 10:
        result.append(i * 3)
print(result) # [60, 45, 33]

### Создание словарей c помощью zip
# dict(zip(keys, values))
# GOOD
keys =   ['Safe',   'Bob',     'Thomas']
values = ['Hammad', 'Builder', 'Engine']
d = dict(zip(keys, values))
print(d) # {'Bob': 'Builder', 'Safe': 'Hammad', 'Thomas': 'Engine'}

# NOT SO GOOD
keys = ['Safe', 'Bob', 'Thomas']
values = ['Hammad', 'Builder', 'Engine']
d = {}
for i, key in enumerate(keys):
    d[key] = values[i]
print(d) # {'Bob': 'Builder', 'Safe': 'Hammad', 'Thomas': 'Engine'}

### Использовать _ для отбрасываемых переменных
for k, _ in [('a', 1), ('b', 2), ('c', 3)]:
    print(k)

### Использовать dict.get() and dict.setdefault()
d = {"a": 1, "b": 2}
d.get("a")
d.get("c", 2)
d["c"] # KeyError: 'c'
d.setdefault("c", 5)
d["c"]

### Сортировка списков
l = [3, 1, 2]
#с использованием функции: создание нового сортированного списка
sorted(l)
#метод объекта sort: сортировка на месте
l.sort()
l

l=[(1,3), (2,2), (3,1)]
l.sort(key=lambda x: x[1])
l
# В качестве параметра key любая функция принимающая одну перменную


### Инверсия порядка элеметов в списке
l = [3, 2, 1]
reversed(l)
l
l.reverse()
l


### Использование функций вместо класса с одним методом
class Dump:
    def __init__(self, var):
        self.var = var
    def action(self):
        print(self.var)

def dump(var):
    def action():
        print(var)
    return action

d = Dump(1)
d.action()

d = dump(2)
d()

### Пользовательские типы данных
# https://docs.python.org/3/library/collections.html
import collections
#collections.namedtuple
Point = collections.namedtuple('Point', ['x', 'y'])
p1 = Point(x=1, y=2)
p2 = Point(11, 22)
p1.x + p2.x

# collections.Counter
c = collections.Counter('gallahad')
c
c.update('aaa')
c

# defaultdict
# https://docs.python.org/3.7/library/collections.html#collections.defaultdict
from collections import defaultdict
sentence = "The red for jumped over the fence and ran to the zoo for food"
words = sentence.split(' ')
d = defaultdict(int)
for word in words:
    d[word] += 1
print(d)

### Модуль itertools
# https://docs.python.org/3/library/itertools.html
from itertools import *
c = 0
for i in cycle('ABCD'):
    print(i, end=' ')
    if c == 10:
        break
    c += 1
else:
    print('No break') # Этот код не будет выполнет
print("\nc =", c)

# Счетчик лучше включать в последовательность с помощью enumerate(cycle('ABCD'))
for i in repeat(10, 3):
    print(i)


### Документирование кода
# docstring
def add1(v):
    """This is very useless  function.
    @v: int - just variable
    @:return int
    """
    return v + 1

help(add1)

# Sphinx генерация документации для питона
# https://pypi.org/project/Sphinx/

# pdoc
# pip install pdoc
# https://pdoc3.github.io/pdoc/

# pydoc
# https://docs.python.org/3.7/library/pydoc.html


## Модули и пакеты

# Общая картина
#  - Повторное использование программного кода
#  - Разделение системы пространств имен
#  - Реализация служб или данных для совместного пользования

### Использование модулей или пакетов
# https://docs.python.org/3/library/os.html
import os
from os import path
from os import path as p


import email
from email.mime import image
from email.mime import audio as ad

# Модуль - это файл
# Пути поиска пакетов и модулей
import sys

sys.path

#### Переменаня окружения PYTHONPATH
# каталог site-packages
# Файлы описания пути *.pth внутри site-packages

#### Модуль site
# https://docs.python.org/3/library/site.html
import site

site.USER_SITE

### Основы программирования модулей
# создание модулей

os.getcwd()
os.chdir("lessons/examples")
sys.path.append(".")

# Пакеты модулей
# __init__.py
import mypackage
import mypackage.work

mypackage.work.action
mypackage.work.action()


### Дополнительные возможности модулей
def tester():
    print('It’s tester...')


if __name__ == '__main__':  # Только когда запускается,
    tester()  # а не импортируется

# Импортирование модулей по имени в виде строки    __import__(modname)
modname = 'mypackage'
try:
    mymodule = __import__(modname)
except ImportError:
    pass
mymodule

# перезагрузка модулей
import importlib

importlib.reload(mypackage)

### Создание пакета для установки
# setup.py
# Создание архива для распространения sdist
# python setup.py sdist

# pip install .
# pip install -e .
# pip uninstall module

# запуск скрипта как модуля
# Создать файл __main__.py в модуле
# python -m python -m script
#> python -m http.server 8000

# Форматы пакетов: egg, wheel
"""
Материал для дополнительного изучения:

Итерируемый объект, итератор и генератор
https://habrahabr.ru/post/337314/  

Генераторы
http://www.dabeaz.com/finalgenerator/

Понимаем декораторы в Python'e, шаг за шагом.
http://habrahabr.ru/post/141411/
http://habrahabr.ru/post/141501/

Python Descriptors Demystified
http://nbviewer.ipython.org/urls/gist.github.com/ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb
                   
Пользовательские атрибуты в Python
http://habrahabr.ru/post/137415/


идиомы питона 
http://habrahabr.ru/post/88972/
http://habrahabr.ru/post/89735/
http://habrahabr.ru/post/90493/
https://python-3-patterns-idioms-test.readthedocs.io/en/latest/


Python Cookbook,Recipes for Mastering Python 3. By Brian Jones, David Beazley 
https://github.com/borisuvarov/python-cookbook-ru

Путеводитель по Python. Пишем великолепный код 
http://habrahabr.ru/post/183912/

Python: советы, уловки, хаки 
http://habrahabr.ru/post/85238/
http://habrahabr.ru/post/85459/
http://habrahabr.ru/post/86706/ 
http://habrahabr.ru/post/95721/

Некоторые возможности Python о которых вы возможно не знали 
http://habrahabr.ru/post/196382/

Вещи, о которых следует помнить, программируя на Python 
http://habrahabr.ru/post/144614/

Python: вещи, которых вы могли не знать 
http://habrahabr.ru/post/207988/

Перестаньте писать классы
https://habrahabr.ru/post/140581/


Интересные особенности Python, о которых вы могли не догадываться
https://habrahabr.ru/post/322360/

Module of the week:
https://pymotw.com/3/

5 распространенных ошибок начинающих программистов на Python
https://habr.com/ru/post/458902/
                   
О порядке поиска пакетов и модулей для импорта в Python 
http://habrahabr.ru/post/166463/

Создание zip-модулей в python 
http://habrahabr.ru/company/acronis/blog/208378/

Python на колёсах
http://habrahabr.ru/post/210450/

Создание python-пакетов 
http://klen.github.io/create-python-packages.html
https://packaging.python.org/

Выкладка python-проектов с помощью pip и wheel 
http://habrahabr.ru/post/172219/

Облегчаем использование pyinstaller для создания exe  
http://habrahabr.ru/post/104589/

pyinstaller  
https://github.com/pyinstaller/pyinstaller/wiki

Как создавать пакеты
https://packaging.python.org/tutorials/distributing-packages
"""
