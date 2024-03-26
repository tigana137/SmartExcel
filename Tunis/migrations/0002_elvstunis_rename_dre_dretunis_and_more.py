# Generated by Django 4.2.7 on 2024-03-15 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tunis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElvsTunis',
            fields=[
                ('uid', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nom_prenom', models.CharField(max_length=200)),
                ('dirty_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameModel(
            old_name='Dre',
            new_name='DreTunis',
        ),
        migrations.RenameModel(
            old_name='Class',
            new_name='ClassTunis',
        ),
        migrations.RenameModel(
            old_name='Ecoles',
            new_name='EcolesTunis',
        ),
        migrations.DeleteModel(
            name='AdminElvs',
        ),
        migrations.AddField(
            model_name='elvstunis',
            name='classe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tunis.classtunis'),
        ),
        migrations.AddField(
            model_name='elvstunis',
            name='ecole',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tunis.ecolestunis'),
        ),
    ]
