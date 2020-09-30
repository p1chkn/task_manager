from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import Task, User
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(author=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['POST'])
def user_register(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if User.objects.filter(username=username).first():
        return Response('User already exist!')
    if username and password:
        User.objects.create_user(username=username, password=password)
        return Response('User created!',status=status.HTTP_201_CREATED)
    else:
        return Response('You need gave password and username.',
                        status=status.HTTP_400_BAD_REQUEST)
