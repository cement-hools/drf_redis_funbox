# drf_redis_funbox
<!---
https://github.com/cement-hools/drf_redis_funbox/badge.svg
--->
![example workflow](https://github.com/cement-hools/drf_redis_funbox/actions/workflows/django.yml/badge.svg)

#### Используется GitHub Actions для автоматического тестирования при изменении кода в репозитории

Приложение должно удовлетворять следующим требованиям. 
- Приложение написано на языке Python версии ~> 3.7. 
- Приложение предоставляет JSON API по HTTP. 
- Приложение предоставляет два HTTP ресурса.
- Для хранения данных сервис должен использовать БД Redis. 
- Код должен быть покрыт тестами.

### Ресурсы
- **POST** ```/visited_links/``` Ресурс загрузки посещений

Ресурс служит для передачи в сервис массива ссылок в POST-запросе. 
Временем их посещения считается время получения запроса сервисом.
#### Тело запроса
```
{
    "links": [
        "https://ya.ru",
        "https://ya.ru?q=123",
        "funbox.ru",
        "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
    ]
}
```
#### Ответ
```
{
    "status": "ok"
}
```

- **GET** ```/visited_domains?from=1545221231&to=1545217638/``` Ресурс загрузки посещений

Ресурс служит для получения GET-запросом списка уникальных доменов,
посещенных за переданный интервал времени. 
Если переменные from и to не заданы, будут выведены все домены из БД
Возможно передать одну переменную (from или to)

#### Ответ
```
{
    "domains": [
        "ya.ru",
        "funbox.ru",
        "stackoverflow.com"
    ],
    "status": "ok"
}
```
## Установка и запуск на сервере разработчика
Подразумевается что в системе установлен и запущен сервер Redis используя 6379 порт

1. Клонировать репозиторий
    ```
    git clone https://github.com/cement-hools/drf_redis_funbox
    ```
2. Перейдите в директорию drf_redis_funbox
    ```
   cd drf_redis_funbox
    ```
3. Создать виртуальное окружение, активировать и установить зависимости
    ``` 
   python -m venv venv
    ```
   Варианты активации окружения:
   - windows ``` venv/Scripts/activate ```
   - linux ``` venv/bin/activate ```
     <br><br>
   ```
   python -m pip install -U pip
   ```
   ```
   pip install -r requirements.txt
   ```
4. Запустить приложение на сервере разработчика
   ```
   python manage.py runserver
   ```
5. Проект доступен 
   ```
   http://localhost:8000/
   ```

## Тесты
```
python manage.py test
```
