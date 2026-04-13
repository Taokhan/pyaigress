# Python FastAPI Project (Poetry)

This project uses **Poetry** for dependency management and **FastAPI** for building APIs.

---

## 🚀 Setup

### 1. Install dependencies

Run this inside the project root:

```bash
poetry install

poetry shell

poetry run uvicorn pyaigress.main:app --reload

🌐 API URLs

Once the server is running:

API: http://127.0.0.1:8000
Swagger Docs: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc


project/
│
├── main.py
├── pyproject.toml
├── poetry.lock
├── README.md
└── .venv/   (if in-project venv is enabled)
