from django.utils import timezone

from test_data import fake
from test_data.companies.robot import create_robot
from companies.models import Company, Robot, Service


def create_robot_service(**fields):
    fake_service_fields = {
        'arrival_datetime': fake.future_datetime(tzinfo=timezone.get_current_timezone()),
        'status': fake.random_element(Service.Status.values),
        'type': fake.random_element(Service.Type.values)
    }

    for field, value in fake_service_fields.items():
        if field not in fields:
            fields[field] = value

    if not fields.get('robot'):
        fields['robot'] = create_robot()

    return Service.objects.create(**fields)
