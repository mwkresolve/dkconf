# Generated by Django 4.0.1 on 2022-11-05 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0024_alter_processes_iptryhack_alter_user_gameip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processes',
            name='iptryhack',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='253.205.110.240', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-11-05 01:18:32.709503'),
        ),
    ]