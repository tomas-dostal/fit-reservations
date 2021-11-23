# Generated by Django 3.2.9 on 2021-11-23 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0008_auto_20211107_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='subgroup',
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reservations.group'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_status',
            field=models.ManyToManyField(blank=True, related_name='reservation_status', to='reservations.ReservationStatus'),
        ),
        migrations.AlterField(
            model_name='room',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.group'),
        ),
        migrations.AlterField(
            model_name='room',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.person'),
        ),
    ]
