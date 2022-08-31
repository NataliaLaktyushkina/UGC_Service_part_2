import logging
import logstash
import random
import sentry_sdk

from flask import Flask, request
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

app.logger.addHandler(logstash.LogstashHandler('logstash', 5044, version=1))
# Handler отвечают за вывод и отправку сообщений. В модуль logging доступно несколько классов-обработчиков
# Например, SteamHandler для записи в поток stdin/stdout, DatagramHandler для UDP, FileHandler для syslog
# LogstashHandler не только отправляет данные по TCP/UDP, но и форматирует логи в json-формат.



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
