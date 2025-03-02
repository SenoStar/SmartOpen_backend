## Запуск проекта на локалке

Win 11

Нужен установленный python на пк.

Перейти в директорию с manage.py

Создать виртуалку питона:
```sh
python -m venv .venv
```

В терминале git bash прописать:
```sh
source .venv/Scripts/activate
```

Если powershell:
```sh
source .\.venv\Scripts\activate 
```

После активации виртуалки скачать зависимости:
```sh
pip install -r req.txt
```

Создать миграции для бд:
```sh
python manage.py makemigrations
```

Сделать таблицы в бд:
```sh
python manage.py migrate
```

Заполнить бд товарами:
```sh
python manage.py fill_db
```

Создать админа:
```sh
python manage.py createsuperuser
```

После ввести нужные данные. Админку будет достпна по ссылке http://127.0.0.1:8000/admin/

Запустить проект:
```sh
python manage.py runserver
```

Доступен по http://127.0.0.1:8000/
