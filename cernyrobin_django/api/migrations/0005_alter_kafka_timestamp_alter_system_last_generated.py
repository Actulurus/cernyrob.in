# Generated by Django 4.2.7 on 2023-12-05 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_job_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kafka',
            name='timestamp',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='system',
            name='last_generated',
            field=models.FloatField(default=0),
        ),
    ]