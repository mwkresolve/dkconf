# Generated by Django 4.0.1 on 2022-11-06 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0029_processes_softdel_alter_user_gameip_alter_user_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='isactive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='207.160.16.8', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-11-06 01:54:39.677429'),
        ),
    ]
