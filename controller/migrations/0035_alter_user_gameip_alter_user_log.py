# Generated by Django 4.0.1 on 2022-11-06 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0034_processes_ismyserver_alter_user_gameip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='193.182.76.107', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-11-06 04:10:14.514290'),
        ),
    ]
