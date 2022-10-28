# Generated by Django 4.0.1 on 2022-10-28 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0018_remove_enigma_solved_enigma_enigma_solved_enigma_ip_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enigma_solved',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='enigma_solved',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='gameip',
            field=models.CharField(default='201.172.247.56', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='log',
            field=models.TextField(default='operating system created at 2022-10-28 19:11:41.629383'),
        ),
    ]