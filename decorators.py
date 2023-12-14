# -*- coding: utf-8 -*-
"""AAA._Python._Decorators.ipynb

# Дектораторы

В этом домашнем задании мы напишем собственные дектораторы,
которые будут менять системные объекты.
Но для начала мы с вами познакомимся с функцией `write`.
"""

import sys
from typing import Callable
from datetime import datetime

sys.stdout.write('Hello, my friend!\n')

"""Это метод объектов file-like классов,
то есть классов, которые реализуют семантику
"Меня можно создать, из меня можно прочитать и в меня можно записать".

Самый главный пример такого объекта -- объект `file`,
являющийся результатом вызова фукнции `open()`.
Для простоты и универсальности взаимодействия,
стандартный ввод и стандартный вывод тоже являются файлами,
из которых можно читать и в которые можно писать.
"""

output = open("./some_test_data.txt", 'w')

output.write('123')

output.close()

"""Как вы могли заметить, функция возвращает число записанных байт.
Это важная часть контракта, которую нужно поддержать,
если вы хотите как-то подменять эту функцию.

## Задача 1

Давайте подменим метод `write` у объекта `sys.stdin` на такую функцию,
которая перед каждым вызовом оригинальной функции записи данных в `stdout`
допечатывает к тексту текущую метку времени.
"""

original_write = sys.stdout.write


def my_write(string_text: str) -> int:
    if len(string_text) == 0 or string_text.isspace():
        text_with_time = string_text
    else:
        text_with_time = (
            datetime.now().strftime('[%Y-%m-%d, %H:%M:%S]: ')
            + string_text
        )
    return original_write(text_with_time)


sys.stdout.write = my_write

print('1, 2, 3')

sys.stdout.write = original_write

"""Вывод должен был бы быть примерно таким:

```
[2021-12-05 12:00:00]: 1, 2, 3
```

## Задача 2

Упакуйте только что написанный код в декторатор.
Весь вывод фукнции должен быть помечен временными метками так, как видно выше.
"""


def timed_output(function: Callable) -> Callable:
    original_write = sys.stdout.write

    def my_write(string_text: str) -> int:
        if len(string_text) == 0 or string_text.isspace():
            text_with_time = string_text
        else:
            timestamp = datetime.now().strftime('[%Y-%m-%d, %H:%M:%S]: ')
            text_with_time = timestamp + string_text
        return original_write(text_with_time)

    def wrapper(*args, **kwargs):
        sys.stdout.write = my_write
        res = function(*args, **kwargs)
        sys.stdout.write = original_write
        return res

    return wrapper


@timed_output
def print_greeting(name):
    print(f'Hello, {name}!')


print_greeting("Nikita")

"""Вывод должен быть похож на следующий:

```
[2021-12-05 12:00:00]: Hello, Nikita!
```

## Задача 3

Напишите декторатор, который будет перенаправлять вывод фукнции в файл.

Подсказка: вы можете заменить объект sys.stdout каким-нибудь другим объектом.
"""


def redirect_output(filepath: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            original_stdout = sys.stdout
            with open(filepath, 'w') as sys.stdout:
                res = func(*args, **kwargs)
            sys.stdout = original_stdout
            return res

        return wrapper

    return decorator


@redirect_output('./function_output.txt')
def calculate() -> None:
    for power in range(1, 5):
        for num in range(1, 20):
            print(num ** power, end=' ')
        print()


calculate()

# Commented out IPython magic to ensure Python compatibility.
# %cat function_output.txt
