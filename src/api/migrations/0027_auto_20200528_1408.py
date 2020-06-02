# Generated by Django 2.2.12 on 2020-05-28 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20200504_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obsquadratbenthicpercent',
            name='percent_algae',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='macroalgae, % cover'),
        ),
        migrations.AlterField(
            model_name='obsquadratbenthicpercent',
            name='percent_hard',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='hard coral, % cover'),
        ),
        migrations.AlterField(
            model_name='obsquadratbenthicpercent',
            name='percent_soft',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='soft coral, % cover'),
        ),
    ]