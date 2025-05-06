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
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        toys_not_associated = Toy.objects.exclude(id_in=instance.toys.all())
        toys_serializer = ToySerializer(toys_not_associated, many=True)
        return Response({
            'monkey': serializer.data,
            'toys_not_associated': toys_serializer.data
        })

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
    
class AddToyToMonkey(APIView):
    def post(self, request, monkey_id, toy_id):
        monkey = Monkey.objects.get(id=monkey_id)
        toy = Toy.objects.get(id=toy_id)
        monkey.toys.add(toy)
        return Response({'message': f'Toy {toy.name} added to Monkey {monkey.name}'})

class RemoveToyFromMonkey(APIView):
    def post(self, request, monkey_id, toy_id):
        monkey = Monkey.objects.get(id=monkey_id)
        toy = Toy.objects.get(id=toy_id)
        monkey.toys.remove(toy)
        return Response({'message': f'Toy {toy.name} removed from Monkey {monkey.name}'})