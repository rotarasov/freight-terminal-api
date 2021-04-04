from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from test_data import fake
from test_data.companies.company import create_company
from test_data.companies.robot import create_robot
from companies.models import Robot
from companies.serializers import RobotSerializer


class CreateNewRobotAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.valid_robot = {
            'model': fake.sentence(2),
            'type': fake.random_element(Robot.Type.values),
            'company': self.company.account.id,
            'status': fake.random_element(Robot.Status.values)
        }
        not_valid_type = fake.sentence(1)
        self.invalid_robot = {
            'model': fake.sentence(2),
            'type': not_valid_type,
            'company': self.company.account.id,
            'status': fake.random_element(Robot.Status.values)
        }

    def test_valid_robot_creation(self):
        response = self.client.post(
            reverse('companies:robot-list', kwargs={'pk': self.company.account.id}), self.valid_robot, format='json')
        robots = Robot.objects.all()
        serializer = RobotSerializer(robots, many=True)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, dict(*serializer.data))

    def test_invalid_robot_creation(self):
        response = self.client.post(
            reverse('companies:robot-list', kwargs={'pk': self.company.account.id}),
            self.invalid_robot, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetRobotAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.robot = create_robot(self.company)

    def test_company_read(self):
        response = self.client.get(
            reverse('companies:robot-detail', kwargs={'company_pk': self.company.account.id, 'robot_pk': self.robot.id}))
        serializer = RobotSerializer(self.robot)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))


class UpdateRobotAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.robot = create_robot(self.company)

        not_valid_status = fake.sentence(1)
        not_valid_type = fake.sentence(2)

        self.valid_partial_data = {
            'status': fake.random_element([s for s in Robot.Status.values if s != self.robot.status])
        }
        self.invalid_partial_data = {
            'status': not_valid_status
        }

        self.valid_data = {
            'model': self.robot.model,
            'type': self.robot.type,
            'company': self.company.account.id,
            'status': self.robot.status
        }

        self.invalid_data = {
            'model': self.robot.model,
            'type': not_valid_type,
            'company': self.company.account.id,
            'status': not_valid_status
        }

    def test_valid_robot_partial_update(self):
        response = self.client.patch(
            reverse('companies:robot-detail', kwargs={'company_pk': self.company.account.id, 'robot_pk': self.robot.id}),
            self.valid_partial_data, format='json')
        self.robot = Robot.objects.get(pk=self.robot.id)
        serializer = RobotSerializer(self.robot)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_robot_partial_update(self):
        response = self.client.patch(
            reverse('companies:robot-detail', kwargs={'company_pk': self.company.account.id, 'robot_pk': self.robot.id}),
            self.invalid_partial_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_robot_update(self):
        response = self.client.put(
            reverse('companies:robot-detail', kwargs={'company_pk': self.company.account.id, 'robot_pk': self.robot.id}),
            self.valid_data, format='json')
        self.robot = Robot.objects.get(pk=self.robot.id)
        serializer = RobotSerializer(self.robot)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, dict(serializer.data))

    def test_invalid_robot_update(self):
        response = self.client.patch(
            reverse('companies:robot-detail', kwargs={'company_pk': self.company.account.id, 'robot_pk': self.robot.id}),
            self.invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteRobotAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.company = create_company()
        self.robot = create_robot(self.company)

    def test_robot_delete(self):
        response = self.client.delete(
            reverse('companies:robot-detail', kwargs={'company_pk': self.company.account.id, 'robot_pk': self.robot.id}),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
