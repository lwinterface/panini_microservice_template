from panini import app as panini_app
from panini.middleware.prometheus_monitoring import PrometheusMonitoringMiddleware
from app.config_manager import get_panini_config, Environment
from app.utils.logging.loki_logger import Logger


panini_config = get_panini_config("remote")
logger = Logger.make_logger(
    panini_config.logging,
    custom_tags={'somekey': 'somevalue'}
)

async def _nats_network_callback(exception):
    logger.error("nats: encountered error")
    logger.exception(exception)
    exit()

app = panini_app.App(
    service_name="template_app",
    servers=panini_config.nats_servers,
    client_nats_name=panini_config.nats_client_name,
    custom_logger=logger,
    error_cb=_nats_network_callback,
)


log = app.logger

message = {
    "key1": "value1",
    "key2": [1, 2, 3, 4],
}


@app.task(interval=2)
async def request_periodically():
    for _ in range(10):
        response = await app.request(subject="some.request.subject", message=message)
        log.info(f"get response from periodic request {response}")

@app.listen("some.request.subject")
async def receive_messages(msg):
    log.info(f"{msg.subject}:{msg.data}")
    return {"success": True, "data": msg.data}


if __name__ == "__main__":
    if 'PROMETHEUS_PUSHGATEWAY_URL' in panini_config.infrastructure:
        app.add_middleware(
            PrometheusMonitoringMiddleware,
            pushgateway_url=panini_config.infrastructure.get('PROMETHEUS_PUSHGATEWAY_URL'),
        )
    app.start()
