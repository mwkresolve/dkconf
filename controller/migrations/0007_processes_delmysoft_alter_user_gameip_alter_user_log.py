# Generated by Django 4.0.1 on 2022-10-26 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0006_processes_uploadip_alter_user_gameip_alter_user_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='processes',
            name='delmysoft',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='14.243.198.214', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-10-26 21:01:55.949055'),
        ),
    ]
