FROM python:3.9.16-buster
# 3.9.16-buster, 3.9-buster
LABEL authors="Marat-77"

WORKDIR /app
RUN apt-get update && apt-get install -y curl
COPY pyproject.toml pyproject.toml
COPY . .
RUN POETRY_VIRTUALENVS_CREATE=false
EXPOSE 5000
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
