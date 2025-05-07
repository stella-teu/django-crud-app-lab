from rest_framework import serializers
from .models import Monkey, Feeding, Toy
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password= validated_data['password']
        )
        return user

class ToySerializer(serializers.ModelSerializer):
    class Meta:
        model = Toy
        fields = '__all__'
        
class MonkeySerializer(serializers.ModelSerializer):
    toys = ToySerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Monkey
        fields = '__all__'

class FeedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeding
        fields = '__all__'
        read_only_fields = ('monkey',)
