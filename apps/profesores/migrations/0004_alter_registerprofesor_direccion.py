# Generated by Django 5.1.2 on 2025-01-29 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesores', '0003_alter_registerprofesor_direccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerprofesor',
            name='direccion',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profesores.direccion'),
        ),
    ]
