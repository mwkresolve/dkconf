# Generated by Django 4.0.1 on 2022-11-06 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0030_software_isactive_alter_user_gameip_alter_user_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='processes',
            name='ipvictim',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='193.123.74.252', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-11-06 02:07:34.805370'),
        ),
    ]
