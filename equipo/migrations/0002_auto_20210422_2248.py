# Generated by Django 3.0.5 on 2021-04-22 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='usuario',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipo',
            name='jugadores',
            field=models.TextField(),
        ),
    ]
