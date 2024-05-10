### Hexlet tests and linter status:
[![Actions Status](https://github.com/pavelkoA/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/pavelkoA/python-project-83/actions)
[![Actions Status](https://github.com/pavelkoA/python-project-83/actions/workflows/project-check.yml/badge.svg)](https://github.com/pavelkoA/python-project-83/actions/workflows/project-check.yml)
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

3. Переиеннуем файл .env.example в .env  
   В DATABASE_URL необходимо вставить данные для подключения к базе банных:
   - USER_DB - пользователь базы данных  
   - PASSWORD_DB - пароль для подключения к базе данных  
   - HOST_DB - хост на котором расположена база (есди на локальном компьютере то localhost или 127.0.0.1)
   - PORT_DB - порт базы данных (поумолчанию 5432)  
   - NAME_DB - имя базы данных  
   В SECRET_KEY необходимо указать секретный ключ (нужен для работы Flask)  

4. Устанавливаем необходимые зависимости и создаем таблицы в базе данных
   Для установки потребуется утилита [poetry](https://python-poetry.org/docs/)
```sh
make build
```

## Ссылка на render.com

[Демонстрационная версия приложения](https://python-project-83-ygm2.onrender.com)
