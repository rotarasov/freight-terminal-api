from math import floor, ceil

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from test_data import fake
from test_data.freights.rule import create_rule
from test_data.freights.state import create_state
from test_data.freights.freight import create_freight
from freights.models import State
from freights.serializers import StateSerializer


class CreateNewStateAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight(need_transfer=True)
        self.rule = create_rule(freight=self.freight)
        self.valid_state = {
            'value': fake.pyfloat(right_digits=2, min_value=floor(self.rule.min_value),
                                  max_value=ceil(self.rule.max_value)),
            'rule': self.rule.id,
        }
        invalid_value = fake.pyfloat(right_digits=2, min_value=ceil(self.rule.device.max_value))
        self.invalid_state = {
            'value': invalid_value,
            'rule': self.rule.id,
        }
        self.state_list_url = reverse('freights:state-list', kwargs={'freight_pk': self.freight.id,
                                                                     'rule_pk': self.rule.id})

    def test_valid_state_creation(self):
        states_before = State.objects.all()

        response = self.client.post(self.state_list_url, self.valid_state, format='json')

        states_after = State.objects.all()
        state = states_after.intersection(states_before).first()
        serializer = StateSerializer(state)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_state_creation(self):
        response = self.client.post(self.state_list_url, self.invalid_state, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetStateAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight(need_transfer=True)
        self.rule = create_rule(freight=self.freight)
        self.state = create_state(rule=self.rule)
        self.state_detail_url = reverse('freights:state-detail', kwargs={'freight_pk': self.freight.id,
                                                                         'rule_pk': self.rule.id,
                                                                         'state_pk': self.state.id})

    def test_state_read(self):
        response = self.client.get(self.state_detail_url)
        serializer = StateSerializer(self.state)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))


class UpdateStateAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight(need_transfer=True)
        self.rule = create_rule(freight=self.freight)
        self.state = create_state(rule=self.rule)

        invalid_value = fake.pyfloat(right_digits=2, min_value=ceil(self.rule.device.max_value))

        self.valid_partial_data = {
            'value': fake.pyfloat(right_digits=2, min_value=ceil(self.rule.min_value),
                                  max_value=floor(self.rule.max_value))
        }
        self.invalid_partial_data = {
            'value': invalid_value
        }
        self.valid_data = {
            'value': fake.pyfloat(right_digits=2, min_value=ceil(self.rule.min_value),
                                  max_value=floor(self.rule.max_value)),
            'rule': self.rule.id
        }
        self.invalid_data = {
            'value': invalid_value,
            'rule': self.rule.id
        }

        self.state_detail_url = reverse('freights:state-detail', kwargs={'freight_pk': self.freight.id,
                                                                         'rule_pk': self.rule.id,
                                                                         'state_pk': self.state.id})

    def test_valid_state_partial_update(self):
        response = self.client.patch(self.state_detail_url, self.valid_partial_data, format='json')
        self.state = State.objects.get(pk=self.state.id)
        serializer = StateSerializer(self.state)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_state_partial_update(self):
        response = self.client.patch(self.state_detail_url, self.invalid_partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_state_update(self):
        response = self.client.put(self.state_detail_url, self.valid_data, format='json')
        self.state = State.objects.get(pk=self.state.id)
        serializer = StateSerializer(self.state)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_state_update(self):
        response = self.client.patch(self.state_detail_url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteStateAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight(need_transfer=True)
        self.rule = create_rule(freight=self.freight)
        self.state = create_state(rule=self.rule)
        self.not_existing_rule_pk = 1000000
        self.state_detail_url = reverse('freights:state-detail', kwargs={'freight_pk': self.freight.id,
                                                                         'rule_pk': self.rule.id,
                                                                         'state_pk': self.state.id})
        self.invalid_state_detail_url = reverse('freights:state-detail', kwargs={'freight_pk': self.freight.id,
                                                                                 'rule_pk': self.not_existing_rule_pk,
                                                                                 'state_pk': self.state.id})

    def test_valid_state_delete(self):
        response = self.client.delete(self.state_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_state_delete(self):
        response = self.client.delete(self.invalid_state_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)