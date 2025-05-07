from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Monkey, Feeding, Toy
from .serializers import UserSerializer, MonkeySerializer, FeedingSerializer, ToySerializer

# Create your views here.
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to monkey collector API home route'}
        return Response(content)

class MonkeyList(generics.ListCreateAPIView):
    serializer_class = MonkeySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Monkey.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MonkeyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MonkeySerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        user = self.request.user
        return Monkey.objects.filter(user=user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        toys_not_associated = Toy.objects.exclude(id_in=instance.toys.all())
        toys_serializer = ToySerializer(toys_not_associated, many=True)
        return Response({
            'monkey': serializer.data,
            'toys_not_associated': toys_serializer.data
        })
    
    def perform_update(self, serializer):
        monkey = self.get_object()
        if monkey.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this cat"})
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this cat"})
        instance.delete()
        
        
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
    

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = User.objects.get(username=request.user)
        refresh = RefreshToken.for_user(request.user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })