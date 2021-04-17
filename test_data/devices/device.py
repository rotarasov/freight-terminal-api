from test_data import fake

from devices.models import Device


def create_device(**fields):
    fake_device_fields = {
        'name': fake.sentence(1),
        'unit': fake.random_element(Device.Unit.values),
        'prefix': fake.random_element(Device.Prefix.values),
        **{k: v for k, v in zip(['min_value', 'max_value'],
                                sorted([fake.pyfloat(right_digits=2), fake.pyfloat(right_digits=2)]))}
    }

    for field, value in fake_device_fields.items():
        if field not in fields:
            fields[field] = value

    return Device.objects.create(**fields)
