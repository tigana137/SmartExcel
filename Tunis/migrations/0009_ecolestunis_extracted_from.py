# Generated by Django 4.2.7 on 2024-03-15 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tunis', '0008_remove_classtunis_class_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecolestunis',
            name='extracted_from',
            field=models.BooleanField(default=False),
        ),
    ]
