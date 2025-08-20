# Task Manager (Flask + Pytest)

Простой CRUD для задач с тестами, Swagger и Docker.

## Стек
- Flask
- SQLAlchemy
- Pytest
- Flasgger (Swagger UI)
- Docker / docker-compose

## Быстрый старт

### 1) Локальный запуск
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

- API: http://127.0.0.1:5000/api/tasks
- Swagger UI: http://127.0.0.1:5000/apidocs/
- Health: http://127.0.0.1:5000/health

### 2) Тесты
```bash
pytest -q
```
Pytest использует in-memory SQLite и создаёт/удаляет таблицы на каждый прогон.

### 3) Docker
```bash
docker-compose up --build
```

## Маршруты
- `POST /api/tasks` — создать задачу `{title, description?, status?}`
- `GET /api/tasks` — список задач
- `GET /api/tasks/<id>` — получить задачу
- `PUT /api/tasks/<id>` — обновить `{title?, description?, status?}`
- `DELETE /api/tasks/<id>` — удалить

# Примеры использования API

## 1. Создать задачу (Create)
curl -X POST http://127.0.0.1:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Сделать тестовое задание",
        "description": "CRUD + тесты + Docker",
        "status": "in_progress"
      }'

Ответ:
{
  "id": 1,
  "title": "Сделать тестовое задание",
  "description": "CRUD + тесты + Docker",
  "status": "in_progress"
}

---

## 2. Получить задачу по ID (Read One)
curl http://127.0.0.1:5000/api/tasks/1

Ответ:
{
  "id": 1,
  "title": "Сделать тестовое задание",
  "description": "CRUD + тесты + Docker",
  "status": "in_progress"
}

---

## 3. Получить список задач (Read List)
curl http://127.0.0.1:5000/api/tasks

Ответ:
[
  {
    "id": 1,
    "title": "Сделать тестовое задание",
    "description": "CRUD + тесты + Docker",
    "status": "in_progress"
  },
  {
    "id": 2,
    "title": "Почитать документацию Flask",
    "description": "",
    "status": "pending"
  }
]

---

## 4. Обновить задачу (Update)
curl -X PUT http://127.0.0.1:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Сделать тестовое задание",
        "status": "done"
      }'

Ответ:
{
  "id": 1,
  "title": "Сделать тестовое задание",
  "description": "CRUD + тесты + Docker",
  "status": "done"
}

---

## 5. Удалить задачу (Delete)
curl -X DELETE http://127.0.0.1:5000/api/tasks/1

Ответ:
{"message": "Task deleted successfully"}

## Качество кода
Проект следует PEP8. Рекомендуемые команды:
```bash
pip install ruff
ruff check .
```

## Замечания
- Значения статуса не ограничены, но можно легко заменить на Enum/валидацию.
- Для БД по умолчанию используется SQLite (файл tasks.db). В прод окружении замените DSN.
