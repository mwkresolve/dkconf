# Generated by Django 4.0.1 on 2022-01-17 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0013_processes_softdownload_alter_user_gameip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='212.192.32.188', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gamepass',
            field=models.CharField(default='W88hkuzL', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-01-17 16:57:43.952258'),
        ),
    ]