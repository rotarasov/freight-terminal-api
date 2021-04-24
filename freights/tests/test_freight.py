from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from test_data import fake
from test_data.companies.service import create_robot_service
from test_data.freights.freight import create_freight
from companies.models import Service
from freights.models import Freight
from freights.serializers import FreightSerializer
from test_data.freights.rule import create_rule
from test_data.freights.state import create_state


class CreateNewFreightAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.delivery_service = create_robot_service(type=Service.Type.DELIVERY)
        self.reception_service = create_robot_service(type=Service.Type.RECEPTION)
        self.valid_freight = {
            'name': fake.sentence(1),
            'status': fake.random_element(Freight.Status.values),
            'transfer': {
                'delivery_service': self.delivery_service.id,
                'reception_service': self.reception_service.id
            },
        }
        not_existing_transfer = 10000000
        self.invalid_freight = {
            'name': fake.sentence(1),
            'status': fake.random_element(Freight.Status.values),
            'transfer': not_existing_transfer
        }
        self.freight_list_url = reverse('freights:list')

    def test_valid_freight_creation(self):
        freights_before = Freight.objects.all()

        response = self.client.post(self.freight_list_url, self.valid_freight, format='json')

        freights_after = Freight.objects.all()
        freight = freights_after.intersection(freights_before).first()
        serializer = FreightSerializer(freight)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_freight_creation(self):
        response = self.client.post(self.freight_list_url, self.invalid_freight, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FreightHealthCheckAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight()
        self.rule = create_rule(freight=self.freight)
        for i in range(20):
            create_state(limit_values=(self.rule.min_value, self.rule.max_value), rule=self.rule)

        self.health_check_url = reverse('freights:check-health', kwargs={'pk': self.freight.id})

    def test_health_check_without_damage(self):
        response = self.client.post(self.health_check_url)
        self.assertFalse(response.data['is_damaged'])

    def test_health_check_with_damage(self):
        for i in range(10):
            create_state(limit_values=(self.rule.max_value, 2 * self.rule.max_value), rule=self.rule)
        response = self.client.post(self.health_check_url)
        self.assertTrue(response.data['is_damaged'])


class GetFreightAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight(need_transfer=True)
        self.freight_detail_url = reverse('freights:detail', kwargs={'pk': self.freight.id})

    def test_rule_read(self):
        response = self.client.get(self.freight_detail_url)
        serializer = FreightSerializer(self.freight)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))


class UpdateFreightAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight(need_transfer=True)
        self.new_delivery_service = create_robot_service(type=Service.Type.DELIVERY)

        not_valid_value = [1, 2, 3, 4]
        not_valid_status = fake.sentence(2)

        self.valid_partial_data = {
            'name': fake.sentence(1)
        }
        self.invalid_partial_data = {
            'name': not_valid_value
        }

        self.valid_data = {
            'name': fake.sentence(1),
            'status': self.freight.status,
            'transfer': {
                'delivery_service': self.new_delivery_service.id,
                'reception_service': self.freight.transfer.reception_service.id,
            },
        }

        self.invalid_data = {
            'name': fake.sentence(1),
            'status': not_valid_status,
            'transfer': {
                'delivery_service': self.freight.transfer.delivery_service.id,
                'reception_service': self.freight.transfer.reception_service.id,
            },
        }

        self.freight_detail_url = reverse('freights:detail', kwargs={'pk': self.freight.id})

    def test_valid_freight_partial_update(self):
        response = self.client.patch(self.freight_detail_url, self.valid_partial_data, format='json')
        self.freight = Freight.objects.get(pk=self.freight.id)
        serializer = FreightSerializer(self.freight)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_freight_partial_update(self):
        response = self.client.patch(self.freight_detail_url, self.invalid_partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_freight_update(self):
        response = self.client.put(self.freight_detail_url, self.valid_data, format='json')
        self.freight = Freight.objects.get(pk=self.freight.id)
        serializer = FreightSerializer(self.freight)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_freight_update(self):
        response = self.client.patch(self.freight_detail_url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteFreightAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight()
        self.not_existing_freight_pk = 1000000
        self.freight_detail_url = reverse('freights:detail', kwargs={'pk': self.freight.id})
        self.invalid_freight_detail_url = reverse('freights:detail', kwargs={'pk': self.not_existing_freight_pk})

    def test_valid_freight_delete(self):
        response = self.client.delete(self.freight_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_freight_delete(self):
        response = self.client.delete(self.invalid_freight_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
