FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY --from=ghcr.io/astral-sh/uv:0.9.9 /uv /uvx /bin/
RUN uv venv
COPY ./alx_travel_app/alx_travel_app/requirements.txt .

RUN uv pip install -r requirements.txt

COPY alx_travel_app/alx_travel_app .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
