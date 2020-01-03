import os

from celery import Celery

REDIS_BROKER_URI = os.environ.get('REDIS_BROKER_URI')
REDIS_BACKEND_URI = os.environ.get('REDIS_BACKEND_URI')


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=REDIS_BROKER_URI,
        broker=REDIS_BACKEND_URI
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
