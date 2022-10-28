# Generated by Django 4.0.1 on 2022-10-27 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0013_enigma_alter_user_gameip_alter_user_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='enigma',
            name='current_ip',
            field=models.CharField(default='', max_length=30000),
        ),
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='98.239.57.160', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-10-27 22:14:39.738254'),
        ),
    ]
