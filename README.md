## API для Yamdb.
### Авторы: Баданов Сергей, Мелентьев Матвей, Баринов Станислав
### Содержание проекта:
- Модели для создания базы данных
- Классы и методы REST для гибкой настройки валидации и доступа:
    ### - подробное описание
    ###
    ###
    ###
    ### - подробное описание
- Административая панель для управления контентом базы данных
### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/hix9/api_yamdb.git
```
Перейти в директорию с проектом.
Команды для Unix систем:
Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
Команды для Windows:
```
py -m venv venv
```

```
source venv/Scripts/activate
```

```
py -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
py manage.py migrate
```

Запустить проект:

```
py manage.py runserver
```
