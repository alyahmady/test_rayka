from django.db import IntegrityError
from django.test import TestCase

from apps.devices.models import DeviceModel, Device


# class DeviceModelTest(TestCase):
#     def setUp(self):
#         self.device_model = DeviceModel.objects.create(name="test")
#
#     def tearDown(self):
#         self.device_model.delete()
#
#     def test_fields(self):
#         self.assertEqual(str(self.device_model), "test")
#
#     def test_unique_name(self):
#         with self.assertRaises(IntegrityError):
#             DeviceModel.objects.create(name="test")
#
#     def test_ordering(self):
#         test_device_model = DeviceModel.objects.create(name="test2")
#         self.assertEqual(
#             DeviceModel.objects.all().first().name,
#             "test2",
#         )
#         test_device_model.delete()
#
#     def test_db_table(self):
#         self.assertEqual(DeviceModel._meta.db_table, "rayka_test_device_models")
#
#
# class DeviceTest(TestCase):
#     def setUp(self):
#         self.device_model = DeviceModel.objects.create(name="test")
#         self.device = Device.objects.create(
#             model_id=self.device_model.pk, name="test", serial="A000000001"
#         )
#
#     def tearDown(self):
#         self.device_model.delete()
#         self.device.delete()
#
#     def test_fields(self):
#         self.assertEqual(str(self.device), "test")
#
#     def test_unique_serial(self):
#         with self.assertRaises(IntegrityError):
#             Device.objects.create(
#                 model_id=self.device_model.pk, name="test2", serial="A000000001"
#             )
#
#     def test_unique_name_and_model(self):
#         with self.assertRaises(IntegrityError):
#             Device.objects.create(
#                 model_id=self.device_model.pk, name="test", serial="A000000002"
#             )
#
#     def test_ordering(self):
#         test_device = Device.objects.create(
#             model=self.device_model, name="test2", serial="A000000002"
#         )
#         self.assertEqual(
#             Device.objects.all().first().name,
#             "test2",
#         )
#         test_device.delete()
#
#     def test_db_table(self):
#         self.assertEqual(Device._meta.db_table, "rayka_test_devices")
#
#     def test_incremental_serial(self):
#         self.assertEqual(self.device.serial, "A000000001")
#         test_device = Device.objects.create(
#             model=self.device_model, name="test2", serial=None
#         )
#         self.assertEqual(test_device.serial, "A000000002")
#
#         Device.objects.create(
#             model=self.device_model, name="test3", serial="A999999999"
#         )
#         test_device = Device.objects.create(
#             model=self.device_model, name="test4", serial=None
#         )
#         self.assertEqual(test_device.serial, "B000000001")
#         test_device.delete()
#
#     def test_null_note(self):
#         self.assertIsNone(self.device.note)
