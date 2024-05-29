# Generated by Django 5.0.6 on 2024-05-27 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0013_alter_prerequisite_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prerequisite',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prerequisite_for', to='registration.course'),
        ),
        migrations.AlterField(
            model_name='prerequisite',
            name='prerequisite_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prerequisites', to='registration.course'),
        ),
    ]
