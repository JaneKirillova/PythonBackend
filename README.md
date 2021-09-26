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

Тесты запускаются из командной строки в папке PythonBackend командой:

` pytest integration_tests.py `
 
 
