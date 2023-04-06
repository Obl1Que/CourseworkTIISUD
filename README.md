# Курсовая работа
### Дисциплина: "Технологии и инструменты систем управления данными"
### Тема курсовой работы: "Программа генерации тестовых запросов"

### На данный момент реализовано:
1. Меню настроек для подключения к БД:

![settings](https://user-images.githubusercontent.com/98952144/230480958-d620ac1c-ba80-4e6b-99bc-2f8ea51d4b9c.png)

2. Меню запросов:

![req1](https://user-images.githubusercontent.com/98952144/230481297-534b97f1-a0df-485b-8536-e19d68aa1159.png)

2.1. Пример исполнения, при выборе 10-ти автоматических INSERT-запросов:

![db_insert](https://user-images.githubusercontent.com/98952144/230482256-cdd69b14-27d9-45c2-a308-49b0c6f37d34.png)

2.2. Пример исполнения, при выборе 2-ух автоматических UPDATE-запросов:

![db_insert](https://user-images.githubusercontent.com/98952144/230483375-3e9e48e3-8998-4056-8623-4496df64d5a5.png)

Log:

![db_insert](https://user-images.githubusercontent.com/98952144/230483462-c7745f38-b11c-400a-9039-fb9856cb73b6.png)

2.3. Пример исполнения, при выборе 11-ти автоматических DELETE-запросов:

![image](https://user-images.githubusercontent.com/98952144/230483668-865e64e0-bad6-43bd-99bd-66ff471be4b6.png)

11-ый запрос выдаёт ошибку, так как в таблице больше нет строк. Оставшиеся запросы будут проигнорированы.

2.4. Пример исполнения, при выборе 1-го ручного запроса:

Вид программы:

![db_insert](https://user-images.githubusercontent.com/98952144/230484923-a39c0c9e-af04-4170-b2f2-ab1fc312e4c2.png)

База данных до исполнения запроса:

![db_insert](https://user-images.githubusercontent.com/98952144/230484816-43990caa-b354-4a20-af1b-44f77aed1337.png)

База данных после исполнения запроса:

![db_insert](https://user-images.githubusercontent.com/98952144/230485074-299c4b31-091e-4778-9d3d-ef779dcdadbc.png)
