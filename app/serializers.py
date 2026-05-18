from rest_framework import serializers
from django.contrib.auth.models import User
from .models import LogAcesso



class LogAcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAcesso
        fields = '__all__'
        read_only_fields = ['usuario', 'criada_em']




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']        





class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)        