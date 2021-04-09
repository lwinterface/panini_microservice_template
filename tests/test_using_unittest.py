from unittest import TestCase

from panini.test_client import TestClient

from app.utils import get_broker

BROKER_HOST, BROKER_PORT = get_broker()


def run_app():
    from app.main import app
    app.start()


class TestApp(TestCase):
    client = TestClient(
        run_app,
        base_nats_url=f"nats://{BROKER_HOST}:{BROKER_PORT}"
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.client.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.stop()

    def test_existing_subject(self):
        response = self.client.request("some.request.subject", {"message": "test"})
        self.assertTrue(response["success"])
        self.assertEqual(response["data"]["message"], "test")

    def test_not_existing_subject(self):
        self.assertRaises(OSError, self.client.request, "not.existing.subject", {"message": "test"})

