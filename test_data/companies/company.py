from test_data import fake, User
from companies.models import Company


def create_account():
    company_account = User.objects.create_user(
        email=fake.email(), password=fake.password(), first_name=fake.first_name(), last_name=fake.last_name())
    return company_account


def create_company():
    company_account = create_account()
    company = Company.objects.create(
        account=company_account, name=fake.sentence(1), type=fake.random_element(Company.Type.values))
    return company
