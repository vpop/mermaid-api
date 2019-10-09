# Generated by Django 2.2.3 on 2019-09-12 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20190515_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beltfish',
            name='transect',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='beltfish_method', to='api.FishBeltTransect', verbose_name='fish belt transect'),
        ),
        migrations.AlterField(
            model_name='benthictransect',
            name='sample_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.SampleEvent'),
        ),
        migrations.AlterField(
            model_name='bleachingquadratcollection',
            name='quadrat',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bleachingquadratcollection_method', to='api.QuadratCollection', verbose_name='bleaching quadrat collection'),
        ),
        migrations.AlterField(
            model_name='fishbelttransect',
            name='sample_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.SampleEvent'),
        ),
        migrations.AlterField(
            model_name='quadratcollection',
            name='sample_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.SampleEvent'),
        ),
    ]