FROM python:3.9.17-slim
# FROM python:3.9.16-buster
# 3.9.16-buster, 3.9-buster
MAINTAINER Marat-77
LABEL authors="Marat-77"

# установить рабочую директорию /app
WORKDIR /app
# Обновление пакетов:
RUN apt-get update && apt-get upgrade -y
# установка curl
RUN apt-get update && apt-get install -y curl
# установка poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -
# RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.2.0
# RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.4.2 python3 -
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.1 python3 -
# COPY pyproject.toml pyproject.toml
# скопировать файлы из текущей папки в контейнер:
COPY . .
# добавить в переменную окружения PATH путь к poetry
ENV PATH=$PATH:/root/.local/bin
# установить переменную окружения POETRY_VIRTUALENVS_CREATE в false
# - не создавать виртуальное окружение
ENV POETRY_VIRTUALENVS_CREATE=false
# установить зависимости:
RUN poetry install
# указать порт 5000 для прослушивания:
# EXPOSE 5050
# команда для запуска flask-приложения при старте контейнера:
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "run:gunicorn_app"]
# CMD ["flask", "db", "upgrade", "&&", "gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "run:gunicorn_app"]
# CMD flask db upgrade && flask create-admin && gunicorn -b 0.0.0.0:$PORT run:gunicorn_app
CMD gunicorn -b 0.0.0.0:$PORT run:gunicorn_app
