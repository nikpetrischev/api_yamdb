
# YaMDB API

Групповой проект курса Яндекс.Практикум, посвященного RestAPI.



## Установка

- Клонируем проект:

```
git clone git@github.com:nikpetrischev/api_yamdb.git
```

- Переходим в директорию проекта:

```
cd api_yamdb/
```

- Создаем виртуальное окружение:

```
python3 -m venv venv
```


- Активируем:

```
source venv/bin/activate
```

- Устанавливаем необходимые библиотеки:

```
pip install -r requirements.txt
```

- Проводим необходимые миграции:

```
python3 api_yamdb/manage.py makemigrations
python3 api_yamdb/manage.py migrate
```

- Стартуем сервер Django:

```
python3 api_yamdb/manage.py runserver
```

- Готово!

## Информация об API

См. redoc:

- при запущенном сервере:

```
localhost:8000/redoc/
```

## Стэк

![Python](https://img.shields.io/badge/Python_3.9-%23254F72?style=for-the-badge&logo=python&logoColor=yellow&labelColor=254f72)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![DRF](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![VSCode](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

##
Разработчики:
- Петрищев Николай
- Золотарев Денис
- Николаев Борис
