# Generated by Django 3.2.9 on 2021-11-07 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_auto_20211107_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='subgroup',
            field=models.ManyToManyField(blank=True, related_name='_reservations_group_subgroup_+', to='reservations.Group'),
        ),
    ]