# Generated by Django 4.0.1 on 2022-11-04 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0022_alter_user_gameip_alter_user_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='30.84.44.74', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-11-04 02:39:37.345919'),
        ),
    ]
