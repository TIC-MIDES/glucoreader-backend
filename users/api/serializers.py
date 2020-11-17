from rest_framework import serializers
from ..models import User
from django.contrib.auth import authenticate


"""Es el serializer usado para iniciar sesion"""
class LoginSerializer(serializers.Serializer):
    cedula = serializers.IntegerField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciales incorrectas")

"""Devuelve los datos pertinentes cuando un usario inicia sesion"""
class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'considerations', 'first_name', 'last_name', 'cedula', 'type', 'max_threshold', 'min_threshold')


class PatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'considerations', 'min_threshold', 'max_threshold')


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'cedula', 'password', 'type', 'doctor', 'considerations',
                  'min_threshold', 'max_threshold')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

