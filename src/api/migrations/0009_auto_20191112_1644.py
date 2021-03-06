# Generated by Django 2.2.3 on 2019-11-12 16:44

from django.db import migrations, models


def migrate_nulls(apps, schema_editor):
    Management = apps.get_model('api', 'Management')
    for m in Management.objects.all():
        m.no_take = False if m.no_take is None else m.no_take
        m.open_access = False if m.open_access is None else m.open_access
        m.periodic_closure = False if m.periodic_closure is None else m.periodic_closure
        m.size_limits = False if m.size_limits is None else m.size_limits
        m.gear_restriction = False if m.gear_restriction is None else m.gear_restriction
        m.species_restriction = False if m.species_restriction is None else m.species_restriction
        m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20191113_0627'),
    ]

    operations = [
        migrations.RunPython(migrate_nulls)
    ]
