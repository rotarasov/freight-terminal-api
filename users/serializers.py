from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['is_superuser']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password:
            self.instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(self.instance, attr, value)
        self.instance.save()

        return self.instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['is_superuser'] = self.user.is_superuser
        return data