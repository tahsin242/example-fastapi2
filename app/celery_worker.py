from celery import Celery
import time

   # Connect Celery to the Redis server we already installed
   # (We use 'redis://localhost:6379/0' because Redis is on the same VM)
celery_app = Celery(
    'worker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

   # This is a sample background task
@celery_app.task(name='app.celery_worker.send_welcome_email')
def send_welcome_email(user_email: str):
    # Simulate a slow email sending process (e.g., connecting to SMTP)
    print(f"Starting to send welcome email to {user_email}...")
    time.sleep(5) # Simulates a 5-second delay
    print(f"Successfully sent welcome email to {user_email}!")
    return {"status": "email sent", "email": user_email}