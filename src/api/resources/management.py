import django_filters
from rest_framework import serializers
from base import (
    BaseAPIFilterSet,
    BaseApiViewSet,
    BaseAPISerializer,
    NullableUUIDFilter,
    ExtendedSerializer,
    ModelNameReadOnlyField,
)
from mixins import ProtectedResourceMixin
from ..models import Management
from ..permissions import UnauthenticatedReadOnlyPermission


def get_rules(obj):
    rules = []
    rules_map = (
        ('gear_restriction', 'Gear Restriction'),
        ('no_take', 'No Take'),
        ('open_access', 'Open Access'),
        ('periodic_closure', 'Periodic Closure'),
        ('size_limits', 'Size Limits'),
        ('species_restriction', 'Species Restriction'),
    )

    for field, display in rules_map:
        if getattr(obj, field) is True:
            rules.append(display)

    return ','.join(rules)


class ManagementExtendedSerializer(ExtendedSerializer):
    project = ModelNameReadOnlyField()
    compliance = ModelNameReadOnlyField()
    parties = serializers.ListField(source='parties.all', child=ModelNameReadOnlyField())
    rules = serializers.SerializerMethodField(source='get_rules')

    class Meta:
        geo_field = 'boundary'
        model = Management
        exclude = []

    def get_rules(self, obj):
        return get_rules(obj)


class ManagementSerializer(BaseAPISerializer):
    rules = serializers.SerializerMethodField(source='get_rules')
    project_name = serializers.SerializerMethodField()
    size = serializers.DecimalField(max_digits=12,
                                    decimal_places=3,
                                    coerce_to_string=False,
                                    allow_null=True,
                                    required=False)

    class Meta:
        geo_field = 'boundary'
        model = Management
        exclude = []
        additional_fields = ['rules', 'project_name']

    def get_rules(self, obj):
        return get_rules(obj)

    def get_project_name(self, obj):
        return obj.project.name


class ManagementFilterSet(BaseAPIFilterSet):
    project = django_filters.UUIDFilter(name='sampleevent__site__project', distinct=True,
                                        label='Associated with project')
    predecessor = NullableUUIDFilter(name='predecessor')
    compliance = NullableUUIDFilter(name='compliance')
    est_year = django_filters.NumericRangeFilter(name='est_year')

    unique = django_filters.CharFilter(method='filter_unique')
    exclude_projects = django_filters.CharFilter(method='filter_not_projects')

    class Meta:
        model = Management
        fields = [
            'project',
            'predecessor',
            'parties',
            'compliance',
            'est_year',
            'no_take',
            'periodic_closure',
            'open_access',
            'size_limits',
            'gear_restriction',
            'species_restriction',
            'unique',
            'exclude_projects',
        ]

    def filter_unique(self, queryset, name, value):

        unique_fields = (
            'name',
            'name_secondary',
            'parties',
            'compliance_id',
            'est_year',
            'boundary',
            'size',
            'no_take',
            'periodic_closure',
            'open_access',
            'size_limits',
            'gear_restriction',
            'species_restriction',
        )
        project_id = value
        group_by = ','.join(['"{}"'.format(uf) for uf in unique_fields])

        sql = """
            "management".id::text IN (
                SELECT id
                FROM (
                    SELECT (agg_managements.ids)[1] AS id, project_ids
                    FROM
                    (
                        SELECT
                            ARRAY_AGG(id::text) AS ids,
                            ARRAY_AGG(project_id::text) AS project_ids
                        FROM
                            management
                        INNER JOIN
                            (
                                SELECT array_to_string(ARRAY_AGG(management_party.name ORDER BY management_party.name), ',') AS parties, management_parties.management_id
                                FROM
                                    management_party
                                INNER JOIN
                                    management_parties
                                ON (management_parties.managementparty_id = management_party.id)

                                GROUP BY
                                    management_parties.management_id
                            ) AS mgmt_parties
                        ON (mgmt_parties.management_id = management.id)
                        GROUP BY {}
                    ) AS agg_managements
                    WHERE
                        NOT('{}' = ANY(agg_managements.project_ids))
                ) AS management_ids
            )
        """.format(group_by, project_id)

        return queryset.extra(where=[sql])

    def filter_not_projects(self, queryset, name, value):
        value_list = [v.strip() for v in value.split(u',')]
        return queryset.exclude(project__in=value_list)


class ManagementViewSet(ProtectedResourceMixin, BaseApiViewSet):
    method_authentication_classes = {
        "GET": []
    }

    model_display_name = "Management Regime"
    serializer_class = ManagementSerializer
    queryset = Management.objects.filter()
    permission_classes = [UnauthenticatedReadOnlyPermission, ]
    filter_class = ManagementFilterSet
    search_fields = ['$name', '$name_secondary', '$project__name', '$est_year']