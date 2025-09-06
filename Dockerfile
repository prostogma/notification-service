FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.19 /uv /uvx /bin/

ADD . /app

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/usr/local/.venv

RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

