# Generated by Django 5.0.3 on 2024-03-29 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0004_alter_destination_accessibility_items_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='caption',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
