# Generated by Django 4.2.7 on 2023-12-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='chunks_completed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='job',
            name='total_chunks',
            field=models.IntegerField(default=0),
        ),
    ]
