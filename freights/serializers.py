from rest_framework import serializers

from freights.models import Freight, Rule, State
from companies.models import Transfer
from companies.serializers import TransferSerializer


class FreightSerializer(serializers.ModelSerializer):
    transfer = TransferSerializer(required=False)

    class Meta:
        model = Freight
        fields = '__all__'

    def create(self, validated_data):
        transfer_data = validated_data.pop('transfer', None)
        freight = Freight.objects.create(**validated_data)
        if transfer_data:
            Transfer.objects.create(freight=freight, **transfer_data)
        return freight

    def update(self, instance, validated_data):
        transfer_data = validated_data.pop('transfer', None)

        if transfer_data:
            if not instance.transfer:
                Transfer.objects.create(freight=instance, **transfer_data)
            else:
                for attr, value in transfer_data.items():
                    setattr(instance.transfer, attr, value)
                instance.transfer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
