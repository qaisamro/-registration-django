# Generated by Django 5.0.4 on 2024-05-24 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(default='defaultpassword', max_length=128),
        ),
    ]