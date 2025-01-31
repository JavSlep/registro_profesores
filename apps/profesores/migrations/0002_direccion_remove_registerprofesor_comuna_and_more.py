# Generated by Django 5.1.2 on 2025-01-29 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pais', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('comuna', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='registerprofesor',
            name='comuna',
        ),
        migrations.RemoveField(
            model_name='registerprofesor',
            name='pais',
        ),
        migrations.RemoveField(
            model_name='registerprofesor',
            name='region',
        ),
        migrations.AlterField(
            model_name='registerprofesor',
            name='direccion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='profesores.direccion'),
        ),
    ]
