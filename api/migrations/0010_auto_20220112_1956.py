# Generated by Django 3.0.5 on 2022-01-12 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20220112_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]
