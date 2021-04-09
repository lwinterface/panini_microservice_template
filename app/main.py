from panini import app as panini_app
from app.utils import get_broker, get_config_path, get_config

BROKER_HOST, BROKER_PORT = get_broker()
CONFIG_PATH = get_config_path()
some_config = get_config('some-config.yml', path=CONFIG_PATH)


app = panini_app.App(
    service_name="template-app",
    host=BROKER_HOST,
    port=BROKER_PORT,
)

log = app.logger

message = {
    "key1": "value1",
    "key2": [1, 2, 3, 4],
}


@app.task()
async def publish():
    for _ in range(10):
        await app.publish(subject="some.request.subject", message=message)
        log.info(f"send message {message}")


@app.timer_task(interval=2)
async def request_periodically():
    for _ in range(10):
        response = await app.request(subject="some.request.subject", message=message)
        log.info(f"get response from periodic request {response}")


@app.listen("some.request.subject")
async def receive_messages(msg):
    log.info(f"got message {msg.subject}:{msg.data}")
    return {"success": True, "data": msg.data}


if __name__ == "__main__":
    app.start()
