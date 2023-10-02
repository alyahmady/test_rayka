from django.conf import settings
from django.test import TestCase, override_settings

from apps.devices.models import Device

from django.test.runner import DiscoverRunner


class NoDatabaseTestRunner(DiscoverRunner):
  def setup_databases(self, **kwargs):
    pass

  def teardown_databases(self, old_config, **kwargs):
    pass


class DeviceTest(TestCase):
    @classmethod
    def setUpClass(cls):
        if not settings.TESTING:
            raise NotImplementedError("You should enable `TESTING_MODE` in env variables.")

        Device.create_table()

    @classmethod
    def tearDownClass(cls):
        if not settings.TESTING:
            raise NotImplementedError("You should enable `TESTING_MODE` in env variables.")

        Device.delete_table()

    def test_device_add_update_get(self):
        Device.add_or_update(
            device_id=123,
            device_model_id=123,
            name="Test Device",
            note="Test Note",
            serial="A000000001",
        )
        device = Device.get(123)

        self.assertIn("id", device)
        self.assertIn("deviceModel", device)
        self.assertIn("name", device)
        self.assertIn("note", device)
        self.assertIn("serial", device)

        Device.delete(123)

    def test_device_get_not_found(self):
        device = Device.get(123)
        self.assertIsNone(device)

    def test_device_delete(self):
        Device.add_or_update(
            device_id=123,
            device_model_id=123,
            name="Test Device",
            note="Test Note",
            serial="A000000001",
        )

        device = Device.get(123)
        self.assertIn("id", device)

        Device.delete(123)

        device = Device.get(123)
        self.assertIsNone(device)

    def test_device_delete_not_found(self):
        device = Device.delete(1235123)
        self.assertIsNone(device)


@override_settings(TESTING=True)
class DeviceAPITest(TestCase):
    @classmethod
    def setUpClass(cls):
        if not settings.TESTING:
            raise NotImplementedError("You should enable `TESTING_MODE` in env variables.")

        Device.create_table()

    @classmethod
    def tearDownClass(cls):
        if not settings.TESTING:
            raise NotImplementedError("You should enable `TESTING_MODE` in env variables.")

        Device.delete_table()

    def test_device_create(self):
        response = self.client.post(
            f"/{settings.API_PREFIX}/{settings.API_VERSION}/devices/",
            {
                "id": "/devices/id123",
                "deviceModel": "/devicemodels/id123",
                "name": "Test Device",
                "note": "Test Note",
                "serial": "A000000001",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": "/devices/id123"})

        Device.delete(123)

    def test_device_create_invalid_serial(self):
        response = self.client.post(
            f"/{settings.API_PREFIX}/{settings.API_VERSION}/devices/",
            {
                "id": "/devices/id123",
                "deviceModel": "/devicemodels/id123",
                "name": "Test Device",
                "note": "Test Note",
                "serial": "000000001",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"serial": ["Serial number must be in the format of A000000001."]},
        )

    def test_device_create_invalid_id(self):
        response = self.client.post(
            f"/{settings.API_PREFIX}/{settings.API_VERSION}/devices/",
            {
                "id": "/devices/123",
                "deviceModel": "/devicemodels/id123",
                "name": "Test Device",
                "note": "Test Note",
                "serial": "A000000001",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"id": ["Device ID is not valid."]})

    def test_device_create_invalid_device_model(self):
        response = self.client.post(
            f"/{settings.API_PREFIX}/{settings.API_VERSION}/devices/",
            {
                "id": "/devices/id123",
                "deviceModel": "/devicemodels/123",
                "name": "Test Device",
                "note": "Test Note",
                "serial": "A000000001",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"deviceModel": ["Device Model ID is not valid."]}
        )

    def test_device_create_invalid_json(self):
        response = self.client.post(
            f"/{settings.API_PREFIX}/{settings.API_VERSION}/devices/",
            {
                "id": "/devices/id123",
                "deviceModel": "/devicemodels/id123",
                "name": "Test Device",
                "note": "Test Note",
                "serial": "A000000001",
            },
            content_type="application/xml",
        )

        self.assertEqual(response.status_code, 415)

    def test_device_get(self):
        Device.add_or_update(
            device_id=123,
            device_model_id=123,
            name="Test Device",
            note="Test Note",
            serial="A000100001",
        )

        response = self.client.get(
            f"/{settings.API_PREFIX}/{settings.API_VERSION}/devices/123/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": "/devices/id123",
                "deviceModel": "/devicemodels/id123",
                "name": "Test Device",
                "note": "Test Note",
                "serial": "A000100001",
            },
        )

        Device.delete(123)

    def test_device_get_not_found(self):
        response = self.client.get(
            f"/{settings.API_PREFIX}/{settings.API_VERSION}/devices/12341236/"
        )

        self.assertEqual(response.status_code, 404)

        response = response.json()
        self.assertIn("message", response)
        self.assertIn("not found", response["message"].lower())

    def test_device_get_invalid_id(self):
        response = self.client.get(
            f"/{settings.API_PREFIX}/{settings.API_VERSION}/devices/abc/"
        )

        self.assertEqual(response.status_code, 404)
