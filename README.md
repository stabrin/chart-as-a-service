# Chart-as-a-Service

Простой, но мощный API-сервис для генерации графиков на лету. Построен на FastAPI и Matplotlib, обернут в Docker для легкого развертывания.

## Возможности

-   **Разные типы графиков**: столбчатые (вертикальные/горизонтальные), линейные, комбинированные (столбцы + линия).
-   **Гибкая настройка**: заголовки, подписи осей, цвета, размеры.
-   **Поддержка нескольких наборов данных** для сравнительных графиков.
-   **Брендирование**: автоматическое добавление водяного знака.
-   **Безопасность**: доступ защищен через API-ключ.
-   **Готов к развертыванию**: полностью настроен с помощью Docker и Docker Compose.

## Быстрый старт (локальный запуск)

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/chart-as-a-service.git
    cd chart-as-a-service
    ```

2.  **Создайте файл с переменными окружения:**
    Скопируйте `example.env` в `.env` и задайте свой секретный ключ.
    ```bash
    cp example.env .env
    ```
    *Содержимое `.env` должно быть таким:*
    ```
    API_KEY=YourSuperSecretKeyGoesHere
    ```

3.  **Запустите сервис с помощью Docker Compose:**
    ```bash
    docker-compose up --build
    ```

4.  **Сервис готов!**
    -   API будет доступен по адресу `http://localhost:8000`.
    -   Интерактивная документация (Swagger UI) доступна по `http://localhost:8000/docs`.

## Как использовать API

Отправьте `POST` запрос на эндпоинт `/generate_chart`.

-   **URL:** `http://localhost:8000/generate_chart`
-   **Метод:** `POST`
-   **Заголовок (Header):** `X-API-Key: YourSuperSecretKeyGoesHere`
-   **Тело запроса (Body):** JSON с описанием графика (см. примеры в документации).

При успешном выполнении сервис вернет изображение в формате PNG.

## Структура проекта

```
.
├── app/                # Основной код приложения на FastAPI
│   ├── core/           # Ядро: схемы, аутентификация, фабрика
│   ├── renderers/      # Модули для отрисовки каждого типа графика
│   └── main.py         # Точка входа FastAPI
├── .env.example        # Пример файла с переменными окружения
├── .gitignore          # Файлы, которые Git должен игнорировать
├── Dockerfile          # Инструкции для сборки Docker-образа
├── docker-compose.yml  # Оркестрация для разработки
└── requirements.txt    # Python-зависимости
```
Полезные команды
git add .
git commit -m "Add logo TabrinSergey"
git push

на боевом сервере
cd project/chart-as-a-service/
git pull
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml logs
docker compose -f docker-compose.prod.yml restart