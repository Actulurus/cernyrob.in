# Generated by Django 4.2.7 on 2023-12-05 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('created', models.DateTimeField(default=0)),
                ('video_url', models.CharField(max_length=70, primary_key=True, serialize=False, unique=True)),
                ('percent_completed', models.IntegerField(default=0)),
                ('chunks_completed', models.IntegerField(default=0)),
                ('total_chunks', models.IntegerField(default=0)),
                ('finished', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Kafka',
            fields=[
                ('video_url', models.CharField(max_length=70, primary_key=True, serialize=False, unique=True)),
                ('video_info', models.JSONField(default=str)),
                ('language', models.CharField(max_length=10)),
                ('transcript', models.CharField(max_length=999999)),
                ('answers', models.CharField(max_length=99999)),
                ('timestamp', models.DateTimeField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20, unique=True)),
                ('last_generated', models.IntegerField(default=0)),
            ],
        ),
    ]
