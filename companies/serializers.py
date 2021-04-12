from rest_framework import serializers

from companies.models import Company, Robot, Service, Transfer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def validate(self, attrs):
        robot = attrs.get('robot')
        service_status = attrs.get('status')

        if self.instance and not robot:
            robot = self.instance.robot

        if robot and robot.status == Robot.Status.UNAVAILABLE:
            raise serializers.ValidationError('Robot is unavailable for a new service.')

        if (robot
                and service_status
                and robot.status == Robot.Status.BUSY
                and service_status != Service.Status.NOT_STARTED):
            raise serializers.ValidationError('Started service can not be set to busy robot.')

        return attrs


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

    def validate_delivery_service(self, value):
        if value.type != Service.Type.DELIVERY:
            raise serializers.ValidationError({'delivery_service': 'Delivery service must have delivery type.'})

        return value

    def validate_reception_service(self, value):
        if value.type != Service.Type.RECEPTION:
            raise serializers.ValidationError({'reception_service': 'Reception service must have reception type.'})

        return value

