Backend

запущен в Yandex.Cloud serverless containers (https://cloud.yandex.ru/solutions/serverless):
https://bba5m8q40e55aukh4h3h.containers.yandexcloud.net/

Реализован на Flask
Получает запросы от frontend с помощью REST API
Отправляет запрос в базу данных Postgres, полученный результат в виде json возвращает на frontend.
Авторизация с помощью JWT: генерируются 2 токена (access и refresh).
