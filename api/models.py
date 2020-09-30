from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Task(models.Model):
    NEW = 'NW'
    PLANNED = 'PL'
    IN_WORK = 'IW'
    DONE = 'DN'
    STATUS_CHOICES = {
        (NEW, 'New'),
        (PLANNED, 'Planned'),
        (IN_WORK, 'In work'),
        (DONE, 'Done'),
    }
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField("Start date", auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=NEW)
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
    NEW = 'NW'
    PLANNED = 'PL'
    IN_WORK = 'IW'
    DONE = 'DN'
    STATUS_CHOICES = {
        (NEW, 'New'),
        (PLANNED, 'Planned'),
        (IN_WORK, 'In work'),
        (DONE, 'Done'),
    }
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='histoty')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField("Start date")
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=NEW)
    finish_date = models.DateField("Finish date", blank=True, null=True)

    def __str__(self):
        return self.title
