from django.utils import timezone

from test_data import fake
from test_data.companies.robot import create_robot
from companies.models import Company, Robot, Service


def create_robot_service(robot=None):
    if not robot:
        robot = create_robot()
    service = Service.objects.create(
        arrival_datetime=fake.future_datetime(tzinfo=timezone.get_current_timezone()), robot=robot,
        delay_time=fake.time_delta(), status=fake.random_element(Service.Status.values),
        type=fake.random_element(Service.Type.values))
    return service
