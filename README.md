### Hexlet tests and linter status:
[![Actions Status](https://github.com/pavelkoA/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/pavelkoA/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/68a6578fe8273b9d9886/maintainability)](https://codeclimate.com/github/pavelkoA/python-project-83/maintainability)


<h1>Анализатор страниц</h1>

Не большое веб приложение, способное произвести начальный анализ сайта
Проверка проходит по таким параметрам как:
- Доступность
- Наличие заголовка сайта
- Наличие заголовка страницы
- Наличие описания сайта

## Содержание
- [Библиотеки](#библиотеки)
- [Установка пакета](#установка-пакета)
- [Ссылка на render.com](#ссылка-render.com)


## Библиотеки
- [Python3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [gunicorn](https://gunicorn.org/)
- [validators](https://validators.readthedocs.io/)
- [requests](https://requests.readthedocs.io/)
- [bs4](https://www.crummy.com/software/BeautifulSoup/)
- [fake-useragent](https://fake-useragent.readthedocs.io/)
- [psycopg2](https://www.psycopg.org/)


## Установка пакета

1. Вводим команду для клонирования репозитория
```sh
git clone git+https://github.com/pavelkoA/python-project-83.git
```

2. Переходим в директорию с программой
```sh
cd python-project-83
```

3. Cоздайте файл .env по аналогии с .env.example.
   В нем должны быть указанны:
   - строка для подключение к базе [PosgreSQL](https://www.postgresql.org/)
   - Секретный ключ

4. Устанавливаем необходимые зависимости и создаем таблицы в базе данных
   Для установки потребуется утилита [poetry](https://python-poetry.org/docs/)
```sh
make build
```

## Ссылка на render.com

[Демонстрационная версия приложения](https://python-project-83-ygm2.onrender.com)