# Generated by Django 4.2.7 on 2023-11-23 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cernyrobin_app', '0002_anonymoususerprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymoususerprofile',
            name='clicks_mult',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='clicks_mult',
            field=models.IntegerField(default=1),
        ),
    ]
