from rest_framework import serializers 
from .models import Customer, Author 

class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Customer
        fields = ('phone_number', 'email', 'username', 'avatar', 'balance', 'password', 'password_confirm')

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError(
                'Password didnt match!'
            )
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                'Password feild must contain alpha and numeric symbols'
            )
        return attrs
    
    def create(self, validated_data):
        user = Customer.objects.create_user(**validated_data)
        return user
    
class CUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('password',)


class AuthorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Author 
        fields = ('author', 'phone_number', 'email', 'username', 'avatar', 'balance', 'password', 'password_confirm')

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise  serializers.ValidationError(
                'Passwords didnt match!'
            )
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                'Password feild must contain alpha and numeric symbols'
            )
        return attrs
    
    def create(self, validated_data):
        user = Author.objects.create_auther(**validated_data)
        return user
    
class AUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author 
        exclude = ('password',)
