# Generated by Django 2.2 on 2020-09-30 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200930_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('NW', 'New'), ('DN', 'Done'), ('IW', 'In work'), ('PL', 'Planned')], default='NW', max_length=2),
        ),
        migrations.CreateModel(
            name='HistoryTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('status', models.CharField(choices=[('NW', 'New'), ('DN', 'Done'), ('IW', 'In work'), ('PL', 'Planned')], default='NW', max_length=2)),
                ('finish_date', models.DateField(blank=True, null=True, verbose_name='Finish date')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histoty', to='api.Task')),
            ],
        ),
    ]
