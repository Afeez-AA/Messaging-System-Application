from flask import Flask, request, Response
from tasks import send_email, log_current_time
from config import Config, RequestFilter  # Import RequestFilter here
import logging

app = Flask(__name__)

logging.basicConfig(filename=Config.LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.addFilter(RequestFilter())  # Use RequestFilter here

@app.route('/message', methods=['GET'])
def message():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        logging.info(f'Received request to send email to {sendmail}')
        send_email.delay(sendmail)
        return 'Email is being sent.', 200

    if talktome is not None:
        logging.info('Received request to log current time')
        log_current_time.delay()
        return 'Logged current time.', 200

    logging.warning('Invalid request received')
    return 'Invalid request.', 400

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        with open(Config.LOG_FILE_PATH, 'r') as f:
            log_contents = f.read()
        return Response(log_contents, mimetype='text/plain')
    except FileNotFoundError:
        logging.error(f'Log file not found at {Config.LOG_FILE_PATH}')
        return 'Log file not found.', 404
    except Exception as e:
        logging.error(f'Error reading log file: {e}')
        return 'Failed to retrieve logs.', 500

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(host='0.0.0.0', port=5000)
