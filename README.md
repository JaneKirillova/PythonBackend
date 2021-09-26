# Приложение для отслеживания покупок

## Инструкция к запуску тестов:
### Юнит-тесты:

В файле есть точка входа в программу, можно запустить так, тогда запустятся все тесты

Можно запускать из командной строки  из папки PythonBackend:

 `python -m unittest unit_tests` - запуск всех тестов из файла
 
 `python -m unittest -v unit_tests` - можно запустить с ключом `-v` для более подробной информации
 
 при помощи следующих комманд можно запустить тесты для конкретной модели:
 
 `python -m unittest unit_tests.TestItem`
 
 `python -m unittest unit_tests.TestUser`
 
 `python -m unittest unit_tests.TestUserContainer`
 
 `python -m unittest unit_tests.TestPurchasesManager`

### Интеграционные тесты:

Перед тем как запускать тесты нужно запустить сервер:

`uvicorn main:app --reload` - по умолчанию у порта номер `8000`, если порт занят то будет ошибка

 `uvicorn main:app --reload --port <your_port_num>` - можно задать нужный номер порта, но тогда в файле `integration_tests.py` в функции `setUp` нужно изменить в ссылке номер порта
 
 Далее запустить тесты можно из файла `integration_tests.py`
 
 
