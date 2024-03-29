# Generated by Django 5.0.1 on 2024-01-24 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cernyrobin_app', '0005_anonymoususerprofile_callme_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymoususerprofile',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
