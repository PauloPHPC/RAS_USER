from rest_framework import serializers
from .models import User

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name', 'email', 'number', 'role','password']

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name', 'email', 'number', 'role']

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'password', 'email']  # Campos que podem ser atualizados

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()

# class RefreshTokenSerializer(serializers.Serializer):
#     refresh = serializers.CharField()
