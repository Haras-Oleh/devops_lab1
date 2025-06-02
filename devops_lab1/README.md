# DevOps Lab 1

Цей проєкт демонструє простий Flask API, що зберігає дані користувачів у PostgreSQL. Усе розгорнуто в контейнерах за допомогою Docker Compose.

## Запуск

```
docker-compose up --build
```

## API

- GET `/users` — отримати список користувачів
- POST `/users` — додати користувача, JSON: `{"name": "Ім'я"}`
