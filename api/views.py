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


@api_view(['POST'])
def user_register(request):
    if request.POST:
        return Response(status=status.HTTP_201_CREATED)