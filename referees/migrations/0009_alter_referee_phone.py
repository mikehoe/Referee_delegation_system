# Generated by Django 5.1.1 on 2024-10-09 11:39

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referees', '0008_remove_referee_licence_alter_referee_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referee',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, null=True, region=None),
        ),
    ]
