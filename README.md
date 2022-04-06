# Описание
Api v1 для проекта api_YaMDb<br>
Позволяет обращаться к базе и получать ответ в формате JSON
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
3. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
4. Выполнить миграции:
```
python3 manage.py migrate
```
5. По желанию загрузить готовую базу командой:
```
python3 manage.py load_data_csv
```
6. Запустить сервер командой
```
python3 manage.py runserver
```
7. Подробное описание отправки запросов и получения ответов на них можно посмотреть на странице:
```
http://127.0.0.1:8000/redoc/
```


Разрабатывали проект:
Кожушкевич Александр - https://github.com/kazhuha
Живов Игорь - https://github.com/Jloogle
Александр Белей - https://github.com/connectoid