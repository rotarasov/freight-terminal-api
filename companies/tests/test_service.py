from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from test_data import fake
from test_data.companies.company import create_company
from test_data.companies.robot import create_robot
from test_data.companies.service import create_robot_service
from companies.models import Robot, Service
from companies.serializers import ServiceSerializer


class CreateNewServiceAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.free_robot = create_robot(company=self.company, status=Robot.Status.FREE)
        self.busy_robot = create_robot(company=self.company, status=Robot.Status.BUSY)
        self.unavailable_robot = create_robot(company=self.company, status=Robot.Status.UNAVAILABLE)

        self.valid_service = {
            'arrival_datetime': fake.future_datetime(tzinfo=timezone.get_current_timezone()),
            'delay_time': fake.time_delta(),
            'robot': self.free_robot.id,
            'status': fake.random_element(Service.Status.values),
            'type': fake.random_element(Service.Type.values)
        }
        self.busy_robot_service = {
            **self.valid_service,
            'robot': self.busy_robot.id,
            'status': Service.Status.NOT_STARTED
        }
        self.invalid_busy_robot_service = {
            **self.busy_robot_service,
            'status': fake.random_element([s for s in Service.Status.values if s != Service.Status.NOT_STARTED])
        }
        self.unavailable_robot_service = {
            **self.valid_service,
            'robot': self.unavailable_robot.id
        }

        self.free_robot_service_list_url = reverse('companies:service-list',
                                                   kwargs={'company_pk': self.company.account.id,
                                                           'robot_pk': self.free_robot.id})
        self.busy_robot_service_list_url = reverse('companies:service-list',
                                                   kwargs={'company_pk': self.company.account.id,
                                                           'robot_pk': self.busy_robot.id})
        self.unavailable_robot_service_list_url = reverse('companies:service-list',
                                                          kwargs={'company_pk': self.company.account.id,
                                                                  'robot_pk': self.unavailable_robot.id})

    def test_valid_service_creation(self):
        response = self.client.post(self.free_robot_service_list_url, self.valid_service, format='json')
        robot = Robot.objects.get(id=self.free_robot.id)
        service = Service.objects.get(**self.valid_service)
        serializer = ServiceSerializer(service)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, dict(serializer.data))
        self.assertEqual(robot.status, Robot.Status.BUSY)

    def test_service_creation_with_busy_robot(self):
        response = self.client.post(self.busy_robot_service_list_url, self.busy_robot_service, format='json')
        service = Service.objects.get(**self.busy_robot_service)
        serializer = ServiceSerializer(service)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_service_creation_with_busy_robot(self):
        response = self.client.post(self.busy_robot_service_list_url, self.invalid_busy_robot_service, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'Started service can not be set to busy robot.')

    def test_invalid_service_creation_with_unavailable_robot(self):
        response = self.client.post(self.unavailable_robot_service_list_url, self.unavailable_robot_service,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'Robot is unavailable for a new service.')


class GetServiceAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.robot = create_robot(company=self.company)
        self.service = create_robot_service(robot=self.robot)
        self.service_detail_url = reverse('companies:service-detail',
                                          kwargs={'company_pk': self.company.account.id,
                                                  'robot_pk': self.robot.id,
                                                  'service_pk': self.service.id})

    def test_company_read(self):
        response = self.client.get(self.service_detail_url)
        serializer = ServiceSerializer(self.service)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))


class UpdateServiceAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.robot = create_robot(company=self.company, status=Robot.Status.FREE)
        self.unavailable_robot = create_robot(company=self.company, status=Robot.Status.UNAVAILABLE)
        self.service = create_robot_service(robot=self.robot)

        not_valid_status = fake.sentence(1)
        not_valid_datetime = 'not valid datetime'

        self.valid_partial_data = {
            'status': fake.random_element([s for s in Service.Status.values if s != self.robot.status])
        }
        self.invalid_partial_data = {
            'status': not_valid_status
        }
        self.invalid_partial_data_with_robot = {
            'robot': self.unavailable_robot.id
        }

        self.valid_data = {
            'arrival_datetime': self.service.arrival_datetime,
            'delay_time': self.service.delay_time,
            'robot': self.robot.id,
            'status': fake.random_element([s for s in Service.Status.values if s != self.robot.status]),
            'type': self.service.type
        }

        self.invalid_data = {
            'arrival_datetime': not_valid_datetime,
            'delay_time': self.service.delay_time,
            'robot': self.robot.id,
            'status': self.service.status,
            'type': self.service.type
        }

        self.service_detail_url = reverse('companies:service-detail',
                                          kwargs={'company_pk': self.company.account.id,
                                                  'robot_pk': self.robot.id,
                                                  'service_pk': self.service.id})

    def test_valid_service_partial_update(self):
        response = self.client.patch(self.service_detail_url, self.valid_partial_data, format='json')
        self.service = Service.objects.get(pk=self.service.id)
        serializer = ServiceSerializer(self.service)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_service_partial_update(self):
        response = self.client.patch(self.service_detail_url, self.invalid_partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_service_update(self):
        response = self.client.put(self.service_detail_url, self.valid_data, format='json')
        self.service = Service.objects.get(pk=self.service.id)
        serializer = ServiceSerializer(self.service)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_service_update(self):
        response = self.client.patch(self.service_detail_url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_service_robot_update(self):
        response = self.client.patch(self.service_detail_url, self.invalid_partial_data_with_robot, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'Robot is unavailable for a new service.')


class DeleteServiceAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.robot = create_robot(company=self.company)
        self.service = create_robot_service(robot=self.robot)
        self.service_detail_url = reverse('companies:service-detail',
                                          kwargs={'company_pk': self.company.account.id,
                                                  'robot_pk': self.robot.id,
                                                  'service_pk': self.service.id})

    def test_robot_delete(self):
        response = self.client.delete(self.service_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
