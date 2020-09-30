from rest_framework import serializers
from .models import Task, HistoryTask


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    author = serializers.CharField(source='author.username', required=False)

    class Meta:
        fields = ['id', 'author', 'title', 'description', 'start_date',
                  'status', 'finish_date']
        read_only_fields = ['author', 'start_date']
        model = Task


class HistoryTaskSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['task', 'title', 'description', 'start_date',
                  'status', 'finish_date']
        read_only_fields = ['task', 'title', 'description', 'start_date',
                            'status', 'finish_date']
        model = HistoryTask
