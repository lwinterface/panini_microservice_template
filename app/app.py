from panini import app as panini_app
from .utils import get_broker, get_config

BROKER_HOST, BROKER_PORT, CONFIG_PATH = get_broker()
some_config = get_config('some-config.yml', path=CONFIG_PATH)


app = panini_app.App(
    service_name="template-app",
    host=BROKER_HOST,
    port=BROKER_PORT,
)

log = app.logger

message = {
    "key1": "value1",
    "key2": 2,
    "key3": 3.0,
    "key4": [1, 2, 3, 4],
    "key5": {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5},
    "key6": {"subkey1": "1", "subkey2": 2, "3": 3, "4": 4, "5": 5},
    "key7": None,
}


@app.task()
async def publish():
    for _ in range(10):
        await app.publish(subject="some.publish.subject", message=message)
        log.info(f"send message {message}")

@app.timer_task(interval=2)
async def publish_periodically():
    for _ in range(10):
        await app.publish(subject="some.publish.subject", message=message)
        log.info(f"send message from periodic task {message}")


@app.listen("some.publish.subject")
async def receive_messages(msg):
    log.info(f"got message {msg.subject}:{msg.data}")


if __name__ == "__main__":
    app.start()
