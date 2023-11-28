from celery.schedules import crontab

from config import celery_app


@celery_app.task()
def validate_user_credit_cards():
    print("Validating user credit cards")
