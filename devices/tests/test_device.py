from math import floor

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from test_data import fake
from test_data.devices.device import create_device
from devices.models import Device
from devices.serializers import DeviceSerializer


class CreateNewDeviceAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.valid_device = {
            'name': fake.sentence(1),
            'unit': fake.random_element(Device.Unit.values),
            'prefix': fake.random_element(Device.Prefix.values),
            **{k: v for k, v in zip(['min_value', 'max_value'],
                                    sorted([fake.pyfloat(right_digits=2), fake.pyfloat(right_digits=2)]))}
        }

        self.invalid_device = {
            **self.valid_device,
            'unit': fake.sentence(1)
        }
        self.device_list_url = reverse('devices:list')

    def test_valid_device_creation(self):
        devices_before = Device.objects.all()

        response = self.client.post(self.device_list_url, self.valid_device, format='json')

        devices_after = Device.objects.all()
        device = devices_after.intersection(devices_before).first()
        serializer = DeviceSerializer(device)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_device_creation(self):
        response = self.client.post(self.device_list_url, self.invalid_device, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetDeviceAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.device = create_device()
        self.device_detail_url = reverse('devices:detail', kwargs={'pk': self.device.id})

    def test_device_read(self):
        response = self.client.get(self.device_detail_url)
        serializer = DeviceSerializer(self.device)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))


class UpdateDeviceAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.device = create_device()

        self.valid_partial_data = {
            'unit': fake.random_element([value for value in Device.Unit.values if value != self.device.unit]),
        }
        self.invalid_partial_data = {
            'unit': fake.sentence(1)
        }
        self.valid_data = {
            'name': self.device.name,
            'unit': self.device.unit,
            'prefix': self.device.prefix,
            'min_value': fake.pyfloat(right_digits=2, max_value=floor(self.device.max_value)),
            'max_value': self.device.max_value,
        }
        self.invalid_data = {
            **self.valid_data,
            'min_value': self.valid_data['max_value'],
            'max_value': self.valid_data['min_value'],
        }

        self.device_detail_url = reverse('devices:detail', kwargs={'pk': self.device.id})

    def test_valid_device_partial_update(self):
        response = self.client.patch(self.device_detail_url, self.valid_partial_data, format='json')
        self.device = Device.objects.get(pk=self.device.id)
        serializer = DeviceSerializer(self.device)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_device_partial_update(self):
        response = self.client.patch(self.device_detail_url, self.invalid_partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_device_update(self):
        response = self.client.put(self.device_detail_url, self.valid_data, format='json')
        self.device = Device.objects.get(pk=self.device.id)
        serializer = DeviceSerializer(self.device)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_device_update(self):
        response = self.client.patch(self.device_detail_url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteDeviceAPITestCase(APITestCase):
    ...