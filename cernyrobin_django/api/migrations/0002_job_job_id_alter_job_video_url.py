# Generated by Django 4.2.7 on 2023-12-05 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_id',
            field=models.CharField(default='', max_length=20, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='video_url',
            field=models.CharField(max_length=700),
        ),
    ]