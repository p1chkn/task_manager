from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'author', 'title', 'description', 'start_date',
                  'status', 'finish_date']
        read_only_fields = ['author']
        model = Task
