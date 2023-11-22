from django.shortcuts import render
from rest_framework import permissions 
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet 
from rest_framework.generics import GenericAPIView 
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination 
from rest_framework.filters import SearchFilter 
from rest_framework_simplejwt.views import TokenObtainPairView 
from django.shortcuts import get_object_or_404 
from django_filters.rest_framework import DjangoFilterBackend
from .tasks import send_auth_activation_email, send_cust_activation_email 
from .serializers import AuthorRegisterSerializer, CustomerRegisterSerializer, CUserSerializer, AUserSerializer
from .models import Customer, Author 
from .permissions import IsAuthor

class CustomerRegisterView(APIView):
    permission_classes = (permissions.AllowAny, ) 

    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_cust_activation_email.delay(user.email, user.activation_code)
            except:
                return Response({'message': 'Registered, but troubles with email', 'data': serializer.data}, status=201)
            return Response(serializer.data, status=201)
        
class AuthorRetisterView(APIView):
    permission_classes = (permissions.AllowAny, ) 

    def post(self, request):
        serializer = AuthorRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_auth_activation_email.delay(user.email, user.activation_code)
            except:
                return Response({'message': 'Registered, but troubles with email', 'data': serializer.data}, status=201)
            return Response(serializer.data, status=201)
        
class CustActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(Customer, activation_code=code)
        user.is_active = True 
        user.activation_code = 'Usde'
        user.save()
        return Response('Account succesfully activated', status=200)
    
class AuthActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(Author, activation_code=code)
        user.is_active = True 
        user.activation_code = 'Usde'
        user.save()
        return Response('Account succesfully activated', status=200)
    
class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )


class StandartPagination(PageNumberPagination):
    page_size = 2 
    page_query_param = 'page'

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CUserSerializer 
    pagination_class = StandartPagination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('username', )
    filterset_fields = ('username', 'balance',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthor()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    
class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AUserSerializer 
    pagination_class = StandartPagination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('username', )
    filterset_fields = ('username', 'balance', )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthor()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    
