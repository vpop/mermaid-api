from django.db import migrations
from ..models.base import SUPERUSER_APPROVED


othercrcp_name = "Others CRCP"
othercrcp_attributes = [
    "53eedd3c-6538-4e93-9f37-54dbda94802c",
    "67230a45-2ca5-400c-95f9-1a4a4ff376f3",
    "6cd7d5dd-8c41-4526-9c35-0545405b28d7",
    "b984e0a9-e3ab-4d6a-8b07-c40de0e67d04",
    "74efa2d7-f678-49cb-8749-f3abfffceac2",
    "26fff300-e233-4db2-bbb0-978d242e01ab",
    "e38752a4-d0e2-43a7-a729-95f2947fa7e5",
    "5dbd3614-b3e3-4282-a941-a70241b67890",
    "0091bb6b-550f-4691-9c66-328a670a3cef",
    "8aed7803-2501-41d1-ae52-d1e032f082c2",
]


def create_othercrcp_grouping(apps, schema_editor):
    FishAttributeView = apps.get_model("api", "FishAttributeView")
    FishGrouping = apps.get_model("api", "FishGrouping")
    FishGroupingRelationship = apps.get_model("api", "FishGroupingRelationship")
    othercrcp_grouping, _ = FishGrouping.objects.get_or_create(name=othercrcp_name, status=SUPERUSER_APPROVED)
    for attribute_id in othercrcp_attributes:
        attribute = FishAttributeView.objects.get(pk=attribute_id)
        FishGroupingRelationship.objects.get_or_create(
            grouping=othercrcp_grouping, attribute=attribute
        )


def delete_othercrcp_grouping(apps, schema_editor):
    FishGrouping = apps.get_model("api", "FishGrouping")
    # Rely on CASCADE to remove relationships
    othercrcp_grouping = FishGrouping.objects.get(name=othercrcp_name, status=SUPERUSER_APPROVED)
    othercrcp_grouping.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0022_auto_20200407_2123'),
    ]

    operations = [
        migrations.RunPython(create_othercrcp_grouping, delete_othercrcp_grouping)
    ]
