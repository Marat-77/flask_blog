# Flask project. Blog.

---

## Архитектура сервисов в облаке

![My Cloud](my_cloud.png)

## Посмотреть результат:

Выполнено развертывание на Yandex.Cloud (https://cloud.yandex.ru/):

https://bbalkbstlke8eqeguonh.containers.yandexcloud.net/

---

Состоит из 3-х компонентов:
- Frontend (https://bbalkbstlke8eqeguonh.containers.yandexcloud.net/)
- Backend (https://bba5m8q40e55aukh4h3h.containers.yandexcloud.net/)
- Database PostgreSQL 14

---

Frontend и Backend работают в Yandex.Cloud Serverless Containers (https://cloud.yandex.ru/services/serverless-containers)

для развертывания
- сначала был создан реестр в Yandex.Cloud Container Registry (https://cloud.yandex.ru/services/container-registry)
- затем созданы docker-образы `sudo docker build . -t cr.yandex/<ID реестра>/<имя образа>:<тег>`
  - для Frontend:
    `/flask_front$ sudo docker build . -t cr.yandex/crpXXXXXXXXXXXXXXXXX/frontend-flask:0.1`
  - для Backend:
    `/flask_backend$ sudo docker build . -t cr.yandex/crpXXXXXXXXXXXXXXXXX/backend-flask:0.1`
- Созданные образы загружены в реестр:
  - `$ docker push cr.yandex/crpXXXXXXXXXXXXXXXXX/frontend-flask:0.1`
  - `$ docker push cr.yandex/crpXXXXXXXXXXXXXXXXX/backend-flask:0.1`
- База данных PostgreSQL 14 запущена с помощью Yandex Managed Service for PostgreSQL (https://cloud.yandex.ru/services/managed-postgresql)
- В Yandex Serverless Containers созданы контейнеры на основе образов, загруженных в Yandex.Cloud Container Registry
  - для контейнера Frontend указаны следующие переменные окружения:
    - CONFIG_NAME - имя конфигурации (ProductionConfig)
    - sk - SECRET_KEY для Flask
    - API_HOST - адрес Backend (https://bba5m8q40e55aukh4h3h.containers.yandexcloud.net/)
    - API_PORT - адрес Backend (443 - порт для https)
    - API_TIMEOUT - timeout в секундах - время ожидания ответа от Backend
  - для контейнера Backend указаны следующие переменные окружения:
    - CONFIG_NAME - имя конфигурации (ProductionConfig)
    - ADMIN_EMAIL - email администратора
    - ADMIN_PASSWD - пароль администратора
    - api_sk - JWT_SECRET_KEY
    - SQLALCHEMY_DATABASE_URI - путь/URI базы данных вида `postgresql://db_user:db_user_password@db_host:db_port/db_name` (`postgresql://exampleuserdb:examplepasswodr@rc1b-XXXXXXXXXXXXXXXX.mdb.yandexcloud.net:6432/db_example`)
  - для некоторых переменных (sk, api_sk, ADMIN_PASSWD, SQLALCHEMY_DATABASE_URI) использовался сервис Yandex Lockbox (https://cloud.yandex.ru/services/lockbox/)

---

## Для запуска контейнеров локально:
```commandline
docker compose up -d
```
