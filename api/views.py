from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTTokenUserAuthentication
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import Task, User, HistoryTask
from .serializers import TaskSerializer, HistoryTaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=status', '=finish_date']

    def get_queryset(self):
        queryset = Task.objects.filter(author=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['GET'])
def history_task(request, task_id):
    auth = JWTAuthentication()
    user = auth.authenticate(request)[0] if auth.authenticate(request) else ''
    task = get_object_or_404(Task, id=task_id)
    if user != task.author:
        return Response('Not allowed', status=status.HTTP_403_FORBIDDEN)
    task_history = HistoryTask.objects.filter(task=task)
    serializer = HistoryTaskSerializer(task_history, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


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
