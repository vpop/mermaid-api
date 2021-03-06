# Generated by Django 2.2.9 on 2020-04-30 16:36

from django.db import migrations
from ..models.view_models import (
    BeltFishObsView,
    BeltFishSUView,
    BeltFishSEView,
)

drop_fb_obs_view = "DROP VIEW IF EXISTS public.vw_beltfish_obs CASCADE;"
drop_fb_su_view = "DROP VIEW IF EXISTS public.vw_beltfish_su CASCADE;"
drop_fb_se_view = "DROP VIEW IF EXISTS public.vw_beltfish_se;"


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_fishgrouping_regions'),
    ]

    operations = [
        migrations.RunSQL(drop_fb_obs_view, BeltFishObsView.sql),
        migrations.RunSQL(BeltFishObsView.sql, drop_fb_obs_view),
        migrations.RunSQL(BeltFishSUView.sql, drop_fb_su_view),
        migrations.RunSQL(BeltFishSEView.sql, drop_fb_se_view),
    ]
