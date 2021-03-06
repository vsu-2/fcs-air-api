# Generated by Django 3.2.2 on 2022-05-14 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
        ('air', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='passengers',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='query',
            name='flight_class',
            field=models.PositiveSmallIntegerField(choices=[('Y', 'Эконом'), ('C', 'Бизнес')]),
        ),
        migrations.AlterField(
            model_name='querytrip',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='query_trips_by_destination', to='geo.city'),
        ),
        migrations.AlterField(
            model_name='querytrip',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='query_trips_by_origin', to='geo.city'),
        ),
        migrations.AlterField(
            model_name='querytrip',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='air.query'),
        ),
    ]
