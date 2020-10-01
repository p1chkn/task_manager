from django.contrib.auth import get_user_model
from django.db import models
from model_utils import Choices

User = get_user_model()


class Task(models.Model):
    STATUS_CHOICES = Choices(
        ('NW', 'New'),
        ('PL', 'Planned'),
        ('IW', 'In work'),
        ('DN', 'Done'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField("Start date", auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES.NW)
    finish_date = models.DateField("Finish date", blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        history = HistoryTask.objects.create(
            task=Task.objects.filter(id=self.id).first(),
            title=self.title,
            description=self.description,
            start_date=self.start_date,
            status=self.status,
            finish_date=self.finish_date
        )
        history.save()

    def __str__(self):
        return self.title


class HistoryTask(models.Model):
    STATUS_CHOICES = Choices(
        ('NW', 'New'),
        ('PL', 'Planned'),
        ('IW', 'In work'),
        ('DN', 'Done'),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='histoty')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField("Start date")
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES.NW)
    finish_date = models.DateField("Finish date", blank=True, null=True)
    change_date = models.DateField("Change date", auto_now_add=True)

    def __str__(self):
        return self.title
