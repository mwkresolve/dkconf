# Generated by Django 4.0.1 on 2022-11-05 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0025_alter_processes_iptryhack_alter_user_gameip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='78.4.185.10', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-11-05 01:19:15.060053'),
        ),
    ]
