from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Monkey
from .serializers import MonkeySerializer

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
