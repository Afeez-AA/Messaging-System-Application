import smtplib
from celery_app import celery_app
from config import Config, RequestFilter  # Import RequestFilter here
from email.mime.text import MIMEText
from datetime import datetime
import logging

logging.basicConfig(filename=Config.LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.addFilter(RequestFilter())  # Use RequestFilter here

@celery_app.task(name='tasks.send_email')
def send_email(recipient):
    msg = MIMEText('This is a test mail for the messaging system. Please work, i don try abeg!!!')
    msg['Subject'] = 'TEST MAIL FROM AFEEZ ADEBOYE HNG11 INTERN'
    msg['From'] = Config.SMTP_USERNAME
    msg['To'] = recipient

    try:
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_USERNAME, recipient, msg.as_string())
        logging.info(f'Email sent successfully to {recipient}')
    except Exception as e:
        error_message = f'Error sending email to {recipient}: {e}'
        logging.error(error_message)
        print(error_message)
        raise send_email.retry(exc=e, countdown=60)  # Retry after 60 seconds

@celery_app.task(name='tasks.log_current_time')
def log_current_time():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(Config.LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f'{current_time}\n')
        logging.info(f'Logged current time: {current_time}')
    except Exception as e:
        error_message = f'Error logging current time: {e}'
        logging.error(error_message)
        print(error_message)

