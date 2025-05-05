from rest_framework import serializers
from .models import Monkey

class MonkeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Monkey
        fields = '__all__'