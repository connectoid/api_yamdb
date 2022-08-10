# Описание
Api v1 для проекта api_YaMDb<br>
Позволяет обращаться к базе и получать ответ в формате JSON
=======
# api_yamdb
api_yamdb
=======
# Описание
Api v1 для проекта api_YaMDb<br>
Позволяет обращаться к базе и получать ответ в формате JSON

# Стек технологий

При разработке использован следущий стек технологий:

Python 3.7<br>
Django 2.2.19<br>
Django Rest Framework<br>
Simple-GWT<br>
PstgreSQL


# Установка
1. Склонировать репозиторий командой:
 ```
 git clone git@github.com:Jloogle/api_yamdb.git
 ```
2. Перейти в папку с проектом, установить виртуальное окружение и активировать его:
```
 python3 -m venv venv
 ```
 ```
 source venv/bin/activate
 ```
3. Создайте файл .env, в котором укажите переменную окружения SECRET_KEY. 
4. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
5. Выполнить миграции:
```
python3 manage.py migrate
```
6. По желанию загрузить готовую базу командой:
```
python3 manage.py load_data_csv
```
7. Запустить сервер командой
```
python3 manage.py runserver
```
8. Подробное описание отправки запросов и получения ответов на них можно посмотреть на странице:
```
http://127.0.0.1:8000/redoc/
```


Разрабатывали проект:<br>
Живов Игорь - https://github.com/Jloogle <br>
Кожушкевич Александр - https://github.com/kazhuha <br>
Александр Белей - https://github.com/connectoid
