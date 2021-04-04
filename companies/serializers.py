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


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
