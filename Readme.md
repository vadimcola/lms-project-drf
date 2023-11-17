Инструкция по работе с Dockerfile и docker-compose

Для запуска проекта 
Собираем образ с помощью команды: docker-compose build
Запустите контейнеры с помощью команды: docker-compose up
Миграции применяются автоматически
После запуска проекта в терминале запускаем команду для создания суперпользователя: 
docker-compose exec app python manage.py add_su

Суперпользователь:
email: test@test.ru
password: 12345