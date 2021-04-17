from math import floor, ceil
from datetime import timedelta

from test_data import fake
from test_data.freights.freight import create_freight
from test_data.devices.device import create_device
from freights.models import Rule


def create_rule(**fields):
    if not fields.get('device'):
        fields['device'] = create_device()

    limit_value_kwargs = {'right_digits': 2, 'min_value': ceil(fields.get('device').min_value),
                          'max_value': floor(fields.get('device').max_value)}
    fake_rule_fields = {
        'coefficient': fake.pyfloat(right_digits=2, min_value=0, max_value=1),
        'possible_deviation': fake.pyfloat(min_value=0, max_value=10),
        'time_interval': timedelta(hours=fake.pyint(max_value=24), minutes=fake.pyint(max_value=60)),
        **{k: v for k, v in zip(['min_value', 'max_value'],
                                sorted([fake.pyfloat(**limit_value_kwargs), fake.pyfloat(**limit_value_kwargs)]))}
    }

    if not fields.get('freight'):
        fields['freight'] = create_freight()

    for field, value in fake_rule_fields.items():
        if field not in fields:
            fields[field] = value

    return Rule.objects.create(**fields)