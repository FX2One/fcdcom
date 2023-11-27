from config import celery_app
from celery.schedules import crontab

@celery_app.task()
def validate_user_credit_cards():
    print("Validating user credit cards")
