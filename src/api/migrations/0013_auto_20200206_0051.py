# Generated by Django 2.2.9 on 2020-02-06 00:51

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200205_2248'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeltFishObsView',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('project_id', models.UUIDField()),
                ('project_name', models.CharField(max_length=255)),
                ('project_status',
                 models.PositiveSmallIntegerField(choices=[(90, 'open'), (80, 'test'), (10, 'locked')], default=90)),
                ('project_notes', models.TextField(blank=True)),
                ('contact_link', models.CharField(max_length=255)),
                ('tags', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('site_id', models.UUIDField()),
                ('site_name', models.CharField(max_length=255)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('site_notes', models.TextField(blank=True)),
                ('country_id', models.UUIDField()),
                ('country_name', models.CharField(max_length=50)),
                ('reef_type', models.CharField(max_length=50)),
                ('reef_zone', models.CharField(max_length=50)),
                ('reef_exposure', models.CharField(max_length=50)),
                ('management_id', models.UUIDField()),
                ('management_name', models.CharField(max_length=255)),
                ('management_name_secondary', models.CharField(max_length=255)),
                ('management_est_year', models.PositiveSmallIntegerField()),
                ('management_size',
                 models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='Size (ha)')),
                ('management_parties', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('management_compliance', models.CharField(max_length=100)),
                ('management_rules', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('management_notes', models.TextField(blank=True)),
                ('sample_event_id', models.UUIDField()),
                ('sample_date', models.DateField()),
                ('sample_time', models.TimeField()),
                ('current_name', models.CharField(max_length=50)),
                ('tide_name', models.CharField(max_length=50)),
                ('visibility_name', models.CharField(max_length=50)),
                ('depth', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='depth (m)')),
                ('sample_event_notes', models.TextField(blank=True)),
                ('sample_unit_id', models.UUIDField()),
                ('number', models.PositiveSmallIntegerField()),
                ('label', models.CharField(blank=True, max_length=50)),
                (
                'transect_len_surveyed', models.PositiveSmallIntegerField(verbose_name='transect length surveyed (m)')),
                ('reef_slope', models.CharField(max_length=50)),
                ('transect_width', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('observers', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('fish_family', models.CharField(max_length=100)),
                ('fish_genus', models.CharField(max_length=100)),
                ('fish_taxon', models.CharField(max_length=100)),
                ('trophic_group', models.CharField(blank=True, max_length=100)),
                ('trophic_level', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('functional_group', models.CharField(blank=True, max_length=100)),
                ('vulnerability', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('biomass_constant_a', models.DecimalField(blank=True, decimal_places=6, max_digits=7, null=True)),
                ('biomass_constant_b', models.DecimalField(blank=True, decimal_places=6, max_digits=7, null=True)),
                ('biomass_constant_c',
                 models.DecimalField(blank=True, decimal_places=6, default=1, max_digits=7, null=True)),
                ('size_bin', models.PositiveSmallIntegerField()),
                ('size', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='size (cm)')),
                ('count', models.PositiveIntegerField(default=1)),
                ('biomass_kgha', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True,
                                                     verbose_name='biomass (kg/ha)')),
                ('observation_notes', models.TextField(blank=True)),
                ('data_policy_beltfish', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'vw_beltfish_obs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BeltFishSEView',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('project_id', models.UUIDField()),
                ('project_name', models.CharField(max_length=255)),
                ('project_status',
                 models.PositiveSmallIntegerField(choices=[(90, 'open'), (80, 'test'), (10, 'locked')], default=90)),
                ('project_notes', models.TextField(blank=True)),
                ('contact_link', models.CharField(max_length=255)),
                ('tags', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('site_id', models.UUIDField()),
                ('site_name', models.CharField(max_length=255)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('site_notes', models.TextField(blank=True)),
                ('country_id', models.UUIDField()),
                ('country_name', models.CharField(max_length=50)),
                ('reef_type', models.CharField(max_length=50)),
                ('reef_zone', models.CharField(max_length=50)),
                ('reef_exposure', models.CharField(max_length=50)),
                ('management_id', models.UUIDField()),
                ('management_name', models.CharField(max_length=255)),
                ('management_name_secondary', models.CharField(max_length=255)),
                ('management_est_year', models.PositiveSmallIntegerField()),
                ('management_size',
                 models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='Size (ha)')),
                ('management_parties', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('management_compliance', models.CharField(max_length=100)),
                ('management_rules', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('management_notes', models.TextField(blank=True)),
                ('sample_date', models.DateField()),
                ('sample_event_notes', models.TextField(blank=True)),
                ('biomass_kgha_avg', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True,
                                                         verbose_name='biomass (kg/ha)')),
                ('biomass_kgha_by_trophic_group_avg',
                 django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('data_policy_beltfish', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'vw_beltfish_se',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BeltFishSUView',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('project_id', models.UUIDField()),
                ('project_name', models.CharField(max_length=255)),
                ('project_status',
                 models.PositiveSmallIntegerField(choices=[(90, 'open'), (80, 'test'), (10, 'locked')], default=90)),
                ('project_notes', models.TextField(blank=True)),
                ('contact_link', models.CharField(max_length=255)),
                ('tags', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('site_id', models.UUIDField()),
                ('site_name', models.CharField(max_length=255)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('site_notes', models.TextField(blank=True)),
                ('country_id', models.UUIDField()),
                ('country_name', models.CharField(max_length=50)),
                ('reef_type', models.CharField(max_length=50)),
                ('reef_zone', models.CharField(max_length=50)),
                ('reef_exposure', models.CharField(max_length=50)),
                ('management_id', models.UUIDField()),
                ('management_name', models.CharField(max_length=255)),
                ('management_name_secondary', models.CharField(max_length=255)),
                ('management_est_year', models.PositiveSmallIntegerField()),
                ('management_size',
                 models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='Size (ha)')),
                ('management_parties', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('management_compliance', models.CharField(max_length=100)),
                ('management_rules', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('management_notes', models.TextField(blank=True)),
                ('sample_date', models.DateField()),
                ('sample_event_notes', models.TextField(blank=True)),
                ('number', models.PositiveSmallIntegerField()),
                (
                'transect_len_surveyed', models.PositiveSmallIntegerField(verbose_name='transect length surveyed (m)')),
                ('reef_slope', models.CharField(max_length=50)),
                ('size_bin', models.PositiveSmallIntegerField()),
                ('biomass_kgha', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True,
                                                     verbose_name='biomass (kg/ha)')),
                (
                'biomass_kgha_by_trophic_group', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('data_policy_beltfish', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'vw_beltfish_su',
                'managed': False,
            },
        ),
        migrations.RemoveField(
            model_name='site',
            name='public',
        ),
    ]