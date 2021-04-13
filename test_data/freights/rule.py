from test_data import fake
from test_data.freights.freight import create_freight
from freights.models import Rule


def create_rule(**fields):
    fake_rule_fields = {
        'coefficient': fake.pyfloat(right_digits=2, min_value=0, max_value=1),
        'possible_deviation': fake.pyfloat(min_value=0, max_value=10),
        'time_interval': '01:00:00',
        **{k: v for k, v in zip(['min_value', 'max_value'],
                                sorted([fake.pyfloat(right_digits=2), fake.pyfloat(right_digits=2)]))}
    }

    if not fields.get('freight'):
        fields['freight'] = create_freight()

    if not fields.get('device'):
        fields['device'] = ...

    for field, value in fake_rule_fields.items():
        if field not in fields:
            fields[field] = value

    return Rule.objects.create(**fields)