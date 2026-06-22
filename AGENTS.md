# Django Video Platform — Учебный проект

## Текущее состояние проекта (на 22 июня 2026)

Проект полностью реализован:
- **Django 6.0.6**, проект `youtube/`
- Приложения: `users` (кастомная модель User), `videos` (модели, API, админка)
- PostgreSQL через `.env` + `config.py`
- `rest_framework` 3.17.1 установлен
- Кастомная модель пользователя `users.User(AbstractUser)`
- `.env` подключён через `config.py`
- SQL-логирование включено
- Dockerfile + docker-compose.yml (PostgreSQL + Redis + app + Celery worker)
- Celery подключён, задача отправки уведомления при лайке
- Seed-данные: 10k пользователей + 100k опубликованных видео

---

## Задание (оригинал)

Необходимо написать приложение для работы с видео: можно получать видео, ставить им лайки и выводить статистику по лайкам пользователей. Функционала мало, но его хватит чтобы разобраться со всеми базовыми концепциями в Django. Акцент на REST API и DRF.

### Сущности

**Video:**
- `owner` (FK → User) — владелец
- `is_published` (bool) — флаг публикации
- `name` (str) — название
- `total_likes` (int) — денормализованное поле (гонки)
- `created_at` (datetime) — дата создания

**VideoFile:**
- `video` (FK → Video)
- `file` (FileField / CharField — путь к файлу)
- `quality` (choice: HD, FHD, UHD)
- Одно Video → много VideoFile с разным качеством

**Like:**
- `video` (FK → Video)
- `user` (FK → User)
- Уникальность: один пользователь = один лайк на видео

### Эндпоинты (6 ручек)

| Метод | Путь | Описание |
|--------|------|----------|
| GET | `/v1/videos/{id}/` | Деталка видео |
| GET | `/v1/videos/` | Список видео (пагинация) |
| POST/DELETE | `/v1/videos/{id}/likes/` | Поставить/убрать лайк |
| GET | `/v1/videos/ids/` | Список ID опубликованных видео (только staff) |
| GET | `/v1/videos/statistics-subquery/` | Статистика через подзапрос (только staff) |
| GET | `/v1/videos/statistics-group-by/` | Статистика через GROUP BY (только staff) |

### Правила доступа

- **Анонимы** — только published
- **Авторизованный владелец** — свои (включая unpublished) + чужие published
- **Staff** — все без ограничений

Формат ответа: `username` владельца, `name`, `total_likes`, `created_at`, список `files` с качеством.

### Лайки

- Только для опубликованных видео
- 1 пользователь = 1 лайк (unique constraint)
- Конкурентный доступ — `select_for_update()`, обработка `IntegrityError`
- POST — поставить, DELETE — убрать
- При лайке/анлайке обновлять `Video.total_likes` (денормализация)

### Статистика (только staff)

Два эндпоинта: `username` + сумма `total_likes` по опубликованным видео:
1. Через **подзапрос** (`Subquery` + `OuterRef`)
2. Через **GROUP BY** (`.values().annotate()`)

### Дополнительно

- **Админка** — контент-администраторы могут добавлять/редактировать видео
- **Dockerfile** — можно без multi-stage
- **SQL-логирование** — вывод всех SQL-запросов в dev-режиме
- **Seed-данные** — 100k опубликованных видео для 10k пользователей (management command)
- **ORM-исследование** — посмотреть SQL для: `all`, `filter`, `exclude`, `save`, `defer`, `only`, `values`, `values_list`, `select_related`, `prefetch_related`, `select_for_update`, `get_or_create`, `count`, `exists`

### База данных

PostgreSQL.

---

## План реализации

Проект уже начат, у тебя есть базовая структура. План идёт от текущего состояния.

### Фаза 0 — Инфраструктура ✅

- [x] Подключить DRF (`pip install djangorestframework`) + добавить `rest_framework` в `INSTALLED_APPS`
- [ ] Dockerfile + docker-compose.yml (будет в конце)
- [x] Подключить `.env` в settings (через `python-dotenv` + `config.py`)
- [x] Включить SQL-логирование в dev-режиме

### Фаза 1 — Custom User Model ✅

- [x] Создать приложение `users`
- [x] Модель `User(AbstractUser)` — пока пустая, без лишних полей
- [x] Указать `AUTH_USER_MODEL = "users.User"` в settings
- [x] Откатить миграцию videos (`migrate videos zero`)
- [x] Создать и применить миграции (сначала users, потом videos)

### Фаза 2 — Модели (доработка)

Что уже поправлено (✅) и что осталось:
- [x] `created_at` — добавлен `auto_now_add=True`
- [x] `total_likes` — добавлен `default=0`
- [x] `Like.related_name` — добавлен `related_name="likes"`
- [x] `Like` — заменить `unique_together` (deprecated) на `UniqueConstraint` (современный подход)
- [x] `VideoFile.quality` — добавить `max_length` и `default`
- [x] `VideoFile.file` — заменить с CharField на FileField (опционально)

### Фаза 3 — Эндпоинты (по нарастающей сложности)

- [x] `GET /v1/videos/ids/` — только staff, flat list ID-шек
- [x] `GET /v1/videos/` и `GET /v1/videos/{id}/` — пагинация, permission-логика, сериализатор с вложенными VideoFile
- [x] `POST/DELETE /v1/videos/{id}/likes/` — `select_for_update`, обработка гонок, обновление total_likes
- [x] Статистика: два эндпоинта — subquery и group by

### Фаза 4 — Админ-панель ✅

- [x] Настроить `ModelAdmin` для Video: list_display, list_filter, search_fields
- [x] Добавить VideoFile inline в Video

### Фаза 5 — Seed-данные ✅

- [x] Management command: 10k users + 100k published videos
- [x] Использовать `bulk_create`, `F()`, `batch_size`

### Фаза 6 — ORM-исследование ✅

- [x] Написать скрипт/команду, которая выполняет каждый метод и выводит `QuerySet.query`

### Фаза 7 — Docker + Celery

- [x] Dockerfile + docker-compose.yml
- [x] Создать `youtube/celery.py` — приложение Celery
- [x] Создать задачу отправки уведомления при лайке
- [x] Подключить задачу к эндпоинту лайков
- [x] Запустить воркер и проверить

---

## Правила работы

- **Sisyphus не модифицирует файлы проекта**, если я однозначно не попрошу его об этом.
- Sisyphus только проверяет код, подсказывает, помогает с планом и отвечает на вопросы.
- Код пишу я сам.

## Заметки

- **DRF** будет использовать ViewSet'ы для списка/деталки и отдельные APIView для статистики/лайков.
