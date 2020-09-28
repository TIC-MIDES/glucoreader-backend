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
        fields = ('id', 'email', 'first_name', 'last_name', 'cedula')

