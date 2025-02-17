# Generated by Django 5.0.3 on 2024-03-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0003_alter_destination_check_in_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='accessibility_items',
            field=models.ManyToManyField(blank=True, null=True, to='destinations.accessibilityitem'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='amenities',
            field=models.ManyToManyField(blank=True, null=True, to='destinations.amenity'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='standout_amenities',
            field=models.ManyToManyField(blank=True, null=True, to='destinations.standoutamenity'),
        ),
    ]
