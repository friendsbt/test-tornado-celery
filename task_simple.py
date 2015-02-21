import time
from celery import Celery
celery = Celery("simple_task", broker="amqp://guest:guest@localhost:5672")
celery.conf.CELERY_RESULT_BACKEND = "amqp"

@celery.task
def sleep(seconds):
    print('sdsds')
    time.sleep(seconds)
    return "sleep 5s"

if __name__ == "__main__":
    celery.start()