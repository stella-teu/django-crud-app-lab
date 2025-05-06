from rest_framework import serializers
from .models import Monkey, Feeding, Toy

class ToySerializer(serializers.ModelSerializer):
    class Meta:
        model = Toy
        fields = '__all__'
        
class MonkeySerializer(serializers.ModelSerializer):
    toys = ToySerializer(many=True, read_only=True)
    class Meta:
        model = Monkey
        fields = '__all__'

class FeedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeding
        fields = '__all__'
        read_only_fields = ('monkey',)
