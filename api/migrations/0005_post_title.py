# Generated by Django 3.0.5 on 2022-01-08 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20220108_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='empty', max_length=200),
        ),
    ]