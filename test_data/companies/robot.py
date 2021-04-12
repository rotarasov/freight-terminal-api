from test_data import fake

from companies.models import Robot
from test_data.companies.company import create_company


def create_robot(**fields):
    fake_robot_fields = {
        'model': fake.sentence(1),
        'type': fake.random_element(Robot.Type.values),
        'status': fake.random_element(Robot.Status.values)
    }

    if not fields.get('company', None):
        fields['company'] = create_company()

    for field, fake_value in fake_robot_fields.items():
        if field not in fields:
            fields[field] = fake_value

    robot = Robot.objects.create(**fields)

    return robot
