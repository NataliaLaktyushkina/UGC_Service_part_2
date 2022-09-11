# Проектная работа 9 спринта

[Репозиторий ugc_sprint_2 (проектная работа 9-го спринта)](https://github.com/NataliaLaktyushkina/ugc_sprint_2)

### Git Actions:
- [Push and pull request](.github/workflows/python.yml)
- [pre-commit](.pre-commit-config.yaml)


### Исследование хранилища ###
[research](/research)

###  API:
Запуск базы данных из папки *MongoDB*:

`docker compose up`

Запуск приложения из корня проекта:

`docker compose up`

http://127.0.0.1/api/openapi#/

### Закладки: ###
Endpoints:
- добавление фильма в закладки;
- удаление фильма из закладок;
- просмотр списка закладок.

### Лайки: ###
Лайки — это оценка к фильму от 0 до 10

Endpoints:

- просмотр средней пользовательской оценки фильма;
- добавление, удаление или изменение оценки.

###  Рецензии: ###
Endpoints:
- добавление рецензии к фильму:
- добавление лайка или дизлайка к рецензии:

Лайк (+1)
Дизлайк (-1)

- просмотр списка рецензий с возможностью гибкой сортировки:

Типы сортировки - по оценке, по дате добавления рецензии


### Логирование: ###
Запуск из папки *logs*:

`docker compose -f docker-compose-elk.yaml up`
[Sentry](https://sentry.io/organizations/natalia-07/issues/)
