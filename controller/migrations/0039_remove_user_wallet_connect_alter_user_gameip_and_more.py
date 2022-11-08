# Generated by Django 4.0.1 on 2022-11-06 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0038_alter_user_gameip_alter_user_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='wallet_connect',
        ),
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='199.208.91.120', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-11-06 20:28:40.282762'),
        ),
    ]