from celery import Celery

app = Celery(
    "core.celery_app",
    broker="amqp://guest:guest@rabbitmq:5672//",
    include=["core.tasks.email_tasks"],
    backend="rpc://",
)