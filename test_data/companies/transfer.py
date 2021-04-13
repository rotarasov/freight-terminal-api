from test_data.companies.service import create_robot_service
from companies.models import Service, Transfer


def create_transfer(**fields):
    if not fields.get('delivery_service'):
        fields['delivery_service'] = create_robot_service(type=Service.Type.DELIVERY)

    if not fields.get('r`eception_service'):
        fields['reception_service'] = create_robot_service(type=Service.Type.RECEPTION)

    return Transfer.objects.create(**fields)
