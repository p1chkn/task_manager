from rest_framework import serializers
from .models import Task, HistoryTask


class StatusCoiceField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(StatusCoiceField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)


class TaskSerializer(serializers.ModelSerializer):
    status = StatusCoiceField(choices=Task.STATUS_CHOICES)
    author = serializers.CharField(source='author.username', required=False)

    class Meta:
        fields = ['id', 'author', 'title', 'description', 'start_date',
                  'status', 'finish_date']
        read_only_fields = ['author', 'start_date']
        model = Task


class HistoryTaskSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['task', 'title', 'description', 'start_date',
                  'status', 'finish_date', 'change_date']
        read_only_fields = ['task', 'title', 'description', 'start_date',
                            'status', 'finish_date', 'change_date']
        model = HistoryTask
