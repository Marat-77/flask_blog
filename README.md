# Flask project. Blog.

---

Установить необходимые зависимости:

```commandline
$ poetry install
```

---

Переименуйте файл **env_example** -> **.env**

```commandline
$ mv env_example .env
```

содержимое файла:

`sk = 'your_secret_key'`

Замените строку *your_secret_key* на ваш секретный ключ.

Секретный ключ можно сгенерировать с помощью `utils/secret_generator.py`

---

Создать БД:

```commandline
$ flask init-db
```

---

Создать тестовых пользователей:

```commandline
$ flask create-users
```

---

Для запуска API:

```commandline
$ run_api.py
```
