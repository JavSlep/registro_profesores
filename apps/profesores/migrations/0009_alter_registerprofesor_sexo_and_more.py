# Generated by Django 5.1.2 on 2025-01-29 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profesores', '0008_alter_registerprofesor_cv_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerprofesor',
            name='sexo',
            field=models.CharField(choices=[('', 'Seleccione un sexo'), ('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Prefiero no decir', 'Prefiero no decir')], max_length=20),
        ),
        migrations.AlterField(
            model_name='registerprofesor',
            name='telefono',
            field=models.IntegerField(max_length=9, verbose_name='Teléfono: 9 1234 5678'),
        ),
    ]
