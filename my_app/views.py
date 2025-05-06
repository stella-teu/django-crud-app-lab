from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Monkey, Feeding, Toy
from .serializers import MonkeySerializer, FeedingSerializer, ToySerializer

# Create your views here.
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to monkey collector API home route'}
        return Response(content)

class MonkeyList(generics.ListCreateAPIView):
    queryset = Monkey.objects.all()
    serializer_class = MonkeySerializer

class MonkeyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Monkey.objects.all()
    serializer_class = MonkeySerializer
    lookup_field = 'id'

class FeedingList(generics.ListCreateAPIView):
    serializer_class = FeedingSerializer
    
    def get_queryset(self):
        monkey_id = self.kwargs['monkey_id']
        return Feeding.objects.filter(monkey_id=monkey_id)
    
    def perform_create(self, serializer):
        monkey_id = self.kwargs['monkey_id']
        monkey = Monkey.objects.get(id=monkey_id)
        serializer.save(monkey=monkey)

class FeedingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedingSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        monkey_id = self.kwargs['monkey_id']
        return Feeding.objects.filter(monkey_id=monkey_id)

class ToyList(generics.ListCreateAPIView):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer

class ToyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer
    lookup_field = 'id'