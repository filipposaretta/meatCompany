# Generated by Django 3.0.5 on 2022-01-12 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20220111_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='ip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('ip_address', models.GenericIPAddressField()),
            ],
        ),
    ]
