import logging

class RequestFilter(logging.Filter):
    def filter(self, record):
        # Exclude werkzeug logs and only allow our specific log messages
        return not record.name.startswith('werkzeug')


class Config:
    BROKER_URL = 'redis://localhost:6379/0'
    RESULT_BACKEND = 'redis://localhost:6379/0'
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'afeeztesthng@gmail.com'
    SMTP_PASSWORD = 'whnoklnikqnedwwv'
    LOG_FILE_PATH = '/var/log/messaging_system.log'



