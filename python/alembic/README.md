# Alembic

Шаблон окружения миграций для async SQLAlchemy (`postgresql+asyncpg`). Метаданные берутся из `common.models.Base`. Пустой autogenerate файл ревизии не создаёт.

Команды запускайте из корня проекта, рядом с `pyproject.toml`. `load_dotenv()` читает `.env` из текущей директории. Онлайн-подключение собирается из переменных:

- `DATABASE_USERNAME`
- `DATABASE_PASSWORD`
- `DATABASE_HOST`
- `DATABASE_PORT`
- `DATABASE_NAME`

Ожидаемая раскладка приложения: пакет моделей лежит в `app/`, декларативная база — `common.models.Base`.

## Команды

Ревизия по различию моделей и базы. Если отличий нет, файл не создаётся.

```bash
uv run alembic revision --autogenerate -m "add users"
```

Пустая ревизия для данных или SQL, который autogenerate не строит.

```bash
uv run alembic revision -m "backfill status"
```

Применить все миграции до головы.

```bash
uv run alembic upgrade head
```

Сдвинуться на одну ревизию вперёд или назад.

```bash
uv run alembic upgrade +1
uv run alembic downgrade -1
```

Откатить все миграции.

```bash
uv run alembic downgrade base
```

Текущая ревизия базы, история и головы веток.

```bash
uv run alembic current
uv run alembic history
uv run alembic history --verbose
uv run alembic heads
```

Показать одну ревизию.

```bash
uv run alembic show <revision>
```

Сравнить схему базы с моделями и завершиться с ненулевым кодом, если есть расхождения.

```bash
uv run alembic check
```

Напечатать SQL до `head`. Для этого в конфиге нужен `sqlalchemy.url`.

```bash
uv run alembic upgrade head --sql
```

Отметить базу как находящуюся на `head`, не выполняя операции из ревизий.

```bash
uv run alembic stamp head
```

Слить две головы в одну ревизию.

```bash
uv run alembic merge -m "merge heads" <rev1> <rev2>
```
