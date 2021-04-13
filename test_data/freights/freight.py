from test_data import fake
from test_data.companies.transfer import create_transfer
from freights.models import Freight


def create_freight(need_transfer=False, **fields):
    fake_freight_fields = {
        'name': fake.sentence(1),
        'status': fake.random_element(Freight.Status.values),
    }

    if need_transfer and not fields.get('transfer'):
        fields['transfer'] = create_transfer()

    for field, value in fake_freight_fields.items():
        if field not in fields:
            fields[field] = value

    return Freight.objects.create(**fields)