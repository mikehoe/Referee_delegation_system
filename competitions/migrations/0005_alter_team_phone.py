# Generated by Django 5.1.1 on 2024-10-09 11:39

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0004_rename_e_mail_team_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, null=True, region=None),
        ),
    ]
