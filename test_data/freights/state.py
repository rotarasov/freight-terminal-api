from test_data import fake
from test_data.freights.rule import create_rule
from freights.models import State


def create_state(limit_values=None, **fields):
    if not limit_values:
        min_value, max_value = sorted([fake.pyfloat(right_digits=2), fake.pyfloat(right_digits=2)])
    else:
        min_value, max_value = limit_values

    fake_state_fields = {
        'value': fake.pyfloat(right_digits=2, min_value=min_value, max_value=max_value),
    }

    if not fields.get('rule'):
        fields['rule'] = create_rule()

    for field, value in fake_state_fields.items():
        if field not in fields:
            fields[field] = value

    return State.objects.create(**fields)
