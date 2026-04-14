# Python FastAPI Project (Poetry)

This project uses **Poetry** for dependency management and **FastAPI** for building APIs.

---

## 🚀 Setup

### 1. Install dependencies

Run this inside the project root:

```bash
poetry install


poetry run uvicorn pyaigress.main:app --reload

🌐 API URLs

API: http://127.0.0.1:8000
Swagger Docs: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc


Migration
Generate your first migration baseline
bashpoetry run alembic revision --autogenerate -m "initial schema"
poetry run alembic upgrade head

Every time you change a model:
bashpoetry run alembic revision --autogenerate -m "describe what changed"
poetry run alembic upgrade head
