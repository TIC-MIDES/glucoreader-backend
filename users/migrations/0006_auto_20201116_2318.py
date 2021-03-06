# Generated by Django 3.1.1 on 2020-11-17 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201107_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='considerations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='max_threshold',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='min_threshold',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
