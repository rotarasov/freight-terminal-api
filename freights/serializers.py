from rest_framework import serializers

from freights.models import Freight, Rule, State
from companies.models import Transfer
from companies.serializers import TransferSerializer


class FreightSerializer(serializers.ModelSerializer):
    transfer = TransferSerializer(required=False)

    class Meta:
        model = Freight
        fields = '__all__'

    def validate_transfer(self, value_dict):
        if Transfer.exists(**value_dict, instance=self.instance):
            raise serializers.ValidationError('Transfer with this services already exists.')
        return value_dict

    def validate(self, attrs):
        coefficient = attrs.get('coefficient', self.instance.coefficient if self.instance else None)
        transfer = attrs.get('transfer', self.instance.transfer if self.instance else None)
        status = attrs.get('status', self.instance.status if self.instance else None)

        current_coefficient_sum = 0
        if self.instance:
            current_coefficient_sum = self.instance.sum_of_rule_coeffs()

        if coefficient and coefficient + current_coefficient_sum > 1:
            raise serializers.ValidationError({
                'coefficient': 'Sum of coefficients in freight rules can not be greater than 1'
            })

        if not transfer and status != Freight.Status.NOT_ASSIGNED:
            raise serializers.ValidationError('Status must be "not_assigned" when transfer is not assigned to freight')

        return attrs

    def create(self, validated_data):
        transfer_data = validated_data.pop('transfer', None)
        freight = Freight.objects.create(**validated_data)
        if transfer_data:
            freight.transfer = Transfer.objects.create(**transfer_data)
            freight.save()
        return freight

    def update(self, instance, validated_data):
        transfer_data = validated_data.pop('transfer', None)

        if transfer_data:
            if not instance.transfer:
                instance.transfer = Transfer.objects.create(**transfer_data)
            else:
                for attr, value in transfer_data.items():
                    if getattr(instance.transfer, attr) != value:
                        setattr(instance.transfer, attr, value)
                instance.transfer.save()

        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                setattr(instance, attr, value)
        instance.save()

        return instance


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'

    def validate(self, attrs):
        device = attrs.get('device', self.instance.device if self.instance else None)
        min_value = attrs.get('min_value', self.instance.min_value if self.instance else None)
        max_value = attrs.get('max_value', self.instance.max_value if self.instance else None)

        if max_value < min_value:
            raise serializers.ValidationError('Max value must be greater than min value')
        if min_value and min_value < device.min_value:
            raise serializers.ValidationError({'min_value': 'Min value can not be less than min value of device.'})
        if max_value and max_value > device.max_value:
            raise serializers.ValidationError({'max_value': 'Max value can not be greater than max value of device.'})

        return attrs


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

    def validate(self, attrs):
        rule = attrs.get('rule')
        value = attrs.get('value')

        if self.instance and not rule:
            rule = self.instance.rule

        if (rule
                and value
                and (value < rule.device.min_value or value > rule.device.max_value)):
            raise serializers.ValidationError({'value': 'Value must be between device min and max values.'})

        return attrs
