from test_data import fake

from companies.models import Robot
from test_data.companies.company import create_company


def create_robot(company=None):
    if not company:
        company = create_company()
    robot = Robot.objects.create(
        model=fake.sentence(1), type=fake.random_element(Robot.Type.values), company=company,
        status=fake.random_element(Robot.Status.values))
    return robot