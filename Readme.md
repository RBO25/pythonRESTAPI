Реализация метода для Rest API с использованием фреймворка Flask.

Метод POST pereval_added добавляет в БД информацию о новом объекте (перевале).

Метод POST submitData добавляет модерацию для каждого нового объекта и меняет поле status.

Метод GET /submitData/<id> получает одну запись (перевал) по её id.

Метод PATCH /submitData/<id> редактирует существующую запись (замена), если она в статусе new, 
                             кроме тех, что содержат в себе ФИО, адрес почты и номер телефона.

Метод GET /submitData/?user__email=<email> получает список данных обо всех объектах, которые
                                           пользователь с почтой <email> отправил на сервер.

Для запуска проекта установить requirements.txt