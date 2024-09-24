# Generated by Django 5.1.1 on 2024-09-24 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0002_alter_competitioninseason_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='competitioninseason',
            options={'ordering': ['-season__name', 'competition__id'], 'verbose_name_plural': 'Competitions in seasons'},
        ),
        migrations.AlterModelOptions(
            name='competitionlevel',
            options={'ordering': ['id']},
        ),
    ]
