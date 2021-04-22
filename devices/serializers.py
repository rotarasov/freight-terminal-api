from rest_framework import serializers

from devices.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

    def validate(self, attrs):
        min_value = attrs.get('min_value', self.instance.min_value if self.instance else None)
        max_value = attrs.get('max_value', self.instance.max_value if self.instance else None)

        if max_value < min_value:
            raise serializers.ValidationError('Max value must be greater than min value')

        return attrs
