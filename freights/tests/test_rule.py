from math import floor, ceil
from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from test_data import fake
from test_data.freights.rule import create_rule
from test_data.freights.freight import create_freight
from test_data.devices.device import create_device
from freights.models import Rule
from freights.serializers import RuleSerializer


class CreateNewRuleAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.device = create_device()
        self.freight = create_freight(need_transfer=True)

        limit_value_kwargs = {'right_digits': 2, 'min_value': ceil(self.device.min_value),
                              'max_value': floor(self.device.max_value)}
        self.valid_rule = {
            'coefficient': fake.pyfloat(right_digits=2, min_value=0, max_value=1),
            'possible_deviation': fake.pyfloat(min_value=0, max_value=10),
            'time_interval': str(timedelta(hours=fake.pyint(max_value=24), minutes=fake.pyint(max_value=60))),
            'device': self.device.id,
            'freight': self.freight.id,
            **{k: v for k, v in zip(['min_value', 'max_value'],
                                    sorted([fake.pyfloat(**limit_value_kwargs), fake.pyfloat(**limit_value_kwargs)]))}
        }
        not_existing_device = 10000000
        self.invalid_rule = {
            **self.valid_rule,
            'device': not_existing_device
        }
        self.rule_list_url = reverse('freights:rule-list', kwargs={'pk': self.freight.id})

    def test_valid_rule_creation(self):
        rules_before = Rule.objects.all()

        response = self.client.post(self.rule_list_url, self.valid_rule, format='json')

        rules_after = Rule.objects.all()
        rule = rules_after.intersection(rules_before).first()
        serializer = RuleSerializer(rule)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_rule_creation(self):
        response = self.client.post(self.rule_list_url, self.invalid_rule, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetRuleAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight(need_transfer=True)
        self.rule = create_rule(freight=self.freight)
        self.rule_detail_url = reverse('freights:rule-detail', kwargs={'freight_pk': self.freight.id,
                                                                       'rule_pk': self.rule.id})

    def test_rule_read(self):
        response = self.client.get(self.rule_detail_url)
        serializer = RuleSerializer(self.rule)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))


class UpdateRuleAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.device = create_device()
        self.freight = create_freight(need_transfer=True)
        self.rule = create_rule(device=self.device, freight=self.freight)

        not_valid_max_value = fake.pyfloat(right_digits=2, min_value=ceil(self.device.max_value))

        self.valid_partial_data = {
            'max_value': fake.pyfloat(right_digits=2, min_value=ceil(self.rule.min_value),
                                      max_value=floor(self.device.max_value))
        }
        self.invalid_partial_data = {
            'max_value': not_valid_max_value
        }
        self.valid_data = {
            'coefficient': self.rule.coefficient,
            'possible_deviation': fake.pyfloat(right_digits=2, min_value=0, max_value=10),
            'time_interval': self.rule.time_interval,
            'device': self.device.id,
            'freight': self.freight.id,
            'min_value': self.rule.min_value,
            'max_value': self.rule.max_value,
        }

        self.invalid_data = {
            **self.valid_data,
            'min_value': self.valid_data['max_value'],
            'max_value': self.valid_data['min_value'],
        }

        self.rule_detail_url = reverse('freights:rule-detail', kwargs={'freight_pk': self.freight.id,
                                                                       'rule_pk': self.rule.id})

    def test_valid_rule_partial_update(self):
        response = self.client.patch(self.rule_detail_url, self.valid_partial_data, format='json')
        self.rule = Rule.objects.get(pk=self.rule.id)
        serializer = RuleSerializer(self.rule)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_rule_partial_update(self):
        response = self.client.patch(self.rule_detail_url, self.invalid_partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_rule_update(self):
        response = self.client.put(self.rule_detail_url, self.valid_data, format='json')
        self.rule = Rule.objects.get(pk=self.rule.id)
        serializer = RuleSerializer(self.rule)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_rule_update(self):
        response = self.client.patch(self.rule_detail_url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteRuleAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.freight = create_freight(need_transfer=True)
        self.rule = create_rule(freight=self.freight)
        self.not_existing_rule_pk = 1000000
        self.rule_detail_url = reverse('freights:rule-detail', kwargs={'freight_pk': self.freight.id,
                                                                       'rule_pk': self.rule.id})
        self.invalid_rule_detail_url = reverse('freights:rule-detail', kwargs={'freight_pk': self.not_existing_rule_pk,
                                                                               'rule_pk': self.rule.id})

    def test_valid_rule_delete(self):
        response = self.client.delete(self.rule_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_rule_delete(self):
        response = self.client.delete(self.invalid_rule_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
