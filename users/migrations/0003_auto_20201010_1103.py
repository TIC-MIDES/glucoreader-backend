# Generated by Django 3.1.1 on 2020-10-10 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cedula',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
