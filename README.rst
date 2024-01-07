FastAPI + SQLAlchemy + Dependency Injector
==================================================

Run
---

Start postgres server:

    docker-compose up -d

run migration

    alembic upgrade head

run application

    uvicorn webapp.application:app
after this you can access application with url `http://localhost:8000`

to create migration file

    alembic revision --autogenerate -m <migration_name>
