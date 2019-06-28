import logging
import django_filters
from base import BaseAPIFilterSet, BaseAPISerializer, BaseApiViewSet, TagField, to_tag_model_instances
from django.db import transaction
from rest_condition import Or
from rest_framework import exceptions, permissions
from rest_framework.decorators import action
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.response import Response
from rest_framework import serializers

from ..models import Project, Site, Management
from ..permissions import *
from ..utils.replace import replace_sampleunit_objs, replace_collect_record_owner
from .project_profile import ProjectProfileSerializer
from .site import SiteSerializer
from .management import ManagementSerializer


logger = logging.getLogger(__name__)


class ProjectSerializer(BaseAPISerializer):
    project_specific_fields = [
        "observer",
        "project_profile",
        "psite",
        "pmanagement",
        "sampleevent",
        "beltfish",
        "benthiclit",
        "benthicpit",
        "habitatcomplexity",
        "benthictransect",
        "fishbelttransect",
        "obstransectbeltfish",
        "obsbenthiclit",
        "obsbenthicpit",
        "obshabitatcomplexity",
        "collectrecords",
        "beltfishtransectmethod",
        "benthiclittransectmethod",
        "benthicpittransectmethod",
        "habitatcomplexitytransectmethod",
    ]

    countries = serializers.SerializerMethodField()
    num_sites = serializers.SerializerMethodField()
    tags = serializers.ListField(source='tags.all', child=TagField(), required=False)

    def __init__(self, *args, **kwargs):
        for field in self.project_specific_fields:
            self._declared_fields.update(
                {
                    "%ss"
                    % field: HyperlinkedIdentityField(
                        lookup_url_kwarg="project_pk", view_name="%s-list" % field
                    )
                }
            )
        super(ProjectSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        p = super(ProjectSerializer, self).create(validated_data)
        request = self.context.get("request")
        pp = ProjectProfile(
            project=p, profile=request.user.profile, role=ProjectProfile.ADMIN
        )
        pp.save()
        return p

    def update(self, instance, validated_data):
        tags_data = []
        if 'tags' in validated_data:
            tags_data = validated_data['tags'].get('all') or []
            del validated_data['tags']
        instance = super(ProjectSerializer, self).update(instance, validated_data)

        tags = to_tag_model_instances([t.name for t in tags_data], instance.updated_by)
        instance.tags.set(*tags)
        return instance

    class Meta:
        model = Project
        exclude = []
        additional_fields = ["countries", "num_sites"]

    def get_countries(self, obj):
        sites = Site.objects.filter(project=obj)
        return sorted(
            list(set([s.country.name for s in sites if s.country is not None]))
        )

    def get_num_sites(self, obj):
        site = Site.objects.filter(project=obj)
        return len(site)



class ProjectFilterSet(BaseAPIFilterSet):
    profile = django_filters.UUIDFilter(
        name="profiles__profile", distinct=True, label="Associated with profile"
    )

    class Meta:
        model = Project
        fields = ["profile"]


class ProjectAuthenticatedUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        doing_site_mr_replace = False
        if hasattr(view, 'action_map') and 'put' in view.action_map:
            if (view.action_map['put'] == 'find_and_replace_sites' or
                    view.action_map['put'] == 'find_and_replace_managements'):
                doing_site_mr_replace = True
        return (request.user.is_authenticated() and
                (request.method in permissions.SAFE_METHODS or
                 request.method == 'POST' or
                 doing_site_mr_replace))


class ProjectViewSet(BaseApiViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [
        Or(
            UnauthenticatedReadOnlyPermission,
            ProjectAuthenticatedUserPermission,
            ProjectDataAdminPermission,
        )
    ]
    method_authentication_classes = {
        "GET": []
    }
    filter_class = ProjectFilterSet
    search_fields = ["$name", "$sites__country__name"]

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[ProjectAuthenticatedUserPermission]
    )
    def create_project(self, request):
        has_validation_errors = False
        validation_errors = {}
        data = request.data
        context = {"request": request}
        save_point_id = transaction.savepoint()

        project_data = data.get("project")
        profiles_data = data.get("profiles") or []
        sites_data = data.get("sites") or []
        managements_data = data.get("managements") or []
        tags_data = data.get('tags') or []

        # Save Project
        project_data["id"] = None
        project_serializer = ProjectSerializer(data=project_data, context=context)
        if project_serializer.is_valid() is False:
            errors = {"Project": project_serializer.errors}
            raise exceptions.ParseError(errors)

        project = project_serializer.save()

        # Save Project Profiles
        for profile_data in profiles_data:
            data = dict(
                id=None,
                project=project.pk,
                profile=profile_data.get("profile"),
                role=profile_data.get("role"),
            )
            pp_serializer = ProjectProfileSerializer(data=data, context=context)
            if pp_serializer.is_valid() is False:
                validation_errors["Users"] = pp_serializer.errors
                has_validation_errors = True
            else:
                pp_serializer.save()

        # Save Sites
        for site_data in sites_data:
            site_data["predecessor"] = site_data["id"]
            site_data["project"] = project.pk
            site_data["id"] = None
            site_serializer = SiteSerializer(data=site_data, context=context)
            if site_serializer.is_valid() is False:
                validation_errors["Sites"] = site_serializer.errors
                has_validation_errors = True
            else:
                site_serializer.save()

        # Save Managements
        for management_data in managements_data:
            management_data["predecessor"] = management_data["id"]
            management_data["project"] = project.pk
            management_data["id"] = None
            mgmt_serializer = ManagementSerializer(
                data=management_data, context=context
            )
            if mgmt_serializer.is_valid() is False:
                validation_errors["Management Regimes"] = mgmt_serializer.errors
                has_validation_errors = True
            else:
                mgmt_serializer.save()

        tags = to_tag_model_instances(tags_data, project.updated_by)
        project.tags.add(*tags)

        if has_validation_errors is True:
            transaction.savepoint_rollback(save_point_id)
            raise exceptions.ParseError(validation_errors)

        transaction.savepoint_commit(save_point_id)
        return Response(project_serializer.data)

    def _find_and_replace_objs(self, request, pk, obj_cls, field, *args, **kwargs):
        project_id = pk
        qp_find_obj_ids = request.data.get("find")
        qp_replace_obj_id = request.data.get("replace")

        if qp_find_obj_ids is None:
            raise exceptions.ValidationError("'find' is required", code=400)

        if qp_replace_obj_id is None:
            raise exceptions.ValidationError("'replace' is required", code=400)

        profile = request.user.profile
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                replace_obj = obj_cls.objects.get(id=qp_replace_obj_id)
                find_objs = obj_cls.objects.filter(
                    id__in=qp_find_obj_ids, project__id=project_id
                )
                results = replace_sampleunit_objs(find_objs, replace_obj, field, profile)
                transaction.savepoint_commit(sid)
            except obj_cls.DoesNotExist:
                msg = "Replace {} {} does not exist".format(field, qp_replace_obj_id)
                logger.error(msg)
                transaction.savepoint_rollback(sid)
                raise exceptions.ValidationError(msg, code=400)
            except Exception as err:
                logger.error(err)
                transaction.savepoint_rollback(sid)
                return Response("Unknown error while replacing {}s".format(field), status=500)

        return Response(results)

    @action(detail=True, methods=["put"])
    def find_and_replace_managements(self, request, pk, *args, **kwargs):
        return self._find_and_replace_objs(request, pk, Management, "management", *args, **kwargs)

    @action(detail=True, methods=["put"])
    def find_and_replace_sites(self, request, pk, *args, **kwargs):
        return self._find_and_replace_objs(request, pk, Site, "site", *args, **kwargs)

    def _get_profile(self, project_id, profile_id):
        try:
            return ProjectProfile.objects.get(
                project_id=project_id, profile_id=profile_id
            ).profile
        except ProjectProfile.DoesNotExist:
            msg = "Profile does not exist in project".format(profile_id)
            logger.error("Profile {} does not exist in project {}".format(profile_id, project_id))
            raise exceptions.ValidationError(msg, code=400)

    @action(detail=True, methods=["put"])
    def transfer_sample_units(self, request, pk, *args, **kwargs):
        project_id = pk
        qp_to_profile_id = request.data.get("to_profile")
        qp_from_profile_id = request.data.get("from_profile")

        if qp_to_profile_id is None:
            raise exceptions.ValidationError("'to_profile' is required", code=400)

        if qp_from_profile_id is None:
            raise exceptions.ValidationError("'from_profile' is required", code=400)

        from_profile = self._get_profile(project_id, qp_from_profile_id)
        to_profile = self._get_profile(project_id, qp_to_profile_id)

        profile = request.user.profile
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                num_transferred = replace_collect_record_owner(
                    project_id, from_profile, to_profile, profile
                )
                transaction.savepoint_commit(sid)
            except Exception as err:
                logger.error(err)
                transaction.savepoint_rollback(sid)
                raise Response("Unknown error while replacing sites", status=500)

        return Response({"num_collect_records_transferred": num_transferred})