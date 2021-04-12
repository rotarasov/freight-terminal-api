from test_data import fake, User
from companies.models import Company


def create_account(**fields):
    fake_account_fields = {
        'email': fake.email(),
        'password': fake.password(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name()
    }

    for field, value in fake_account_fields.items():
        if field not in fields:
            fields[field] = value

    return User.objects.create_user(**fields)


def create_company(**fields):
    fake_company_fields = {
        'name': fake.sentence(1),
        'type': fake.random_element(Company.Type.values)
    }

    if not fields.get('account'):
        fields['account'] = create_account()

    for field, value in fake_company_fields.items():
        if field not in fields:
            fields[field] = value

    return Company.objects.create(**fields)
