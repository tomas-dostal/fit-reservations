# Generated by Django 3.2.9 on 2021-12-18 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_alter_person_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='locked',
            field=models.BooleanField(default=True),
        ),
    ]
