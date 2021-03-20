"""
Скрипт создает оглавление для всех файлов уроков.

С помощью этого оглавления можно быстро найти в каком файле
расположена интересующая тема.

Заголовком считается строка которая начинается с 
нескольких символов комментария (минимум 2).

Текст заголовока от символов комментария должен отделяться, 
как минимум, одним пробелом.

Запускать в том же каталоге, где находятся уроки.
"""
import glob

LESSONS = '0?.py'
TOCFILE = 'toc.md'

with open(TOCFILE, 'w', encoding='UTF8') as toc:
    for file in glob.glob(LESSONS):
        toc.write(f'# {file}\n')
        for linum, line in enumerate(open(file, encoding='UTF8')):
            if not line.startswith('##'):
                continue
            line = line.strip()
            toc.write(f'{line} : {linum + 1}\n')
        toc.write(f'\n{"-" * 60}\n')
