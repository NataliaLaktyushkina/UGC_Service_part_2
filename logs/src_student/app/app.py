import logging
import random

import logstash
import sentry_sdk
from flask import Flask
from flask import request
from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(integrations=[FlaskIntegration()])
#
sentry_sdk.init(
    dsn="https://bdac46e09f9444d1a209a8e570f92255@o1386750.ingest.sentry.io/6707192",
    integrations=[FlaskIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

app = Flask(__name__)
app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)

logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


app.logger.addFilter(RequestIdFilter())
app.logger.addHandler(logstash_handler)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is requred')


@app.route('/')
def index():
    result = random.randint(1, 50)
    app.logger.info(f'Пользователю досталось число {result}')
    return f"Ваше число {result}!"
