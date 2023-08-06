from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from huscy.projects.models import Project
from huscy.recruitment.models import AttributeFilterSet, Participation
from huscy.recruitment.serializer import (
    AttributeFilterSetSerializer,
    ContactHistorySerializer,
    ParticipationSerializer,
    SubjectGroupSerializer,
)
from huscy.recruitment.services import (
    apply_attribute_filterset,
    create_subject_group,
    get_contact_history,
    get_participations_for_project,
    get_subject_groups,
)
from huscy.subjects.models import Subject
from huscy.subjects.serializers import SubjectSerializer


class ProjectViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Project.objects.all()

    @action(detail=True, methods=['get'])
    def participations(self, request, pk=None):
        project = self.get_object()
        participations = get_participations_for_project(project)
        return Response(data=ParticipationSerializer(participations, many=True).data)


class SubjectGroupViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                          mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = SubjectGroupSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])

    def get_queryset(self):
        return get_subject_groups(self.project)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.project
        return context

    def list(self, request, *args, **kwargs):
        subject_groups = self.get_queryset()
        if not subject_groups:
            subject_groups = [
                create_subject_group(self.project, name='SubjectGroup1', description='')
            ]
        serializer = self.get_serializer(subject_groups, many=True)
        return Response(serializer.data)


class AttributeFilterSetViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = AttributeFilterSet.objects.all()
    serializer_class = AttributeFilterSetSerializer

    @action(detail=True, methods=['get'])
    def apply(self, request, pk=None):
        attribute_filterset = self.get_object()
        subjects = apply_attribute_filterset(attribute_filterset)
        return Response(data=SubjectSerializer(subjects, many=True).data)


class ParticipationViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Subject.objects.all()
    serializer_class = ParticipationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['attribute_filterset'] = get_object_or_404(AttributeFilterSet,
                                                           pk=self.kwargs['attributefilterset_pk'])
        context['subject'] = self.get_object()
        return context

    @action(detail=True, methods=['put'])
    def not_reached(self, request, pk, attributefilterset_pk):
        data = dict(status=Participation.STATUS.get_value('pending'))
        participation_serializer = self.get_serializer(data=data)
        participation_serializer.is_valid(raise_exception=True)
        participation_serializer.save()
        return Response(data=participation_serializer.data)

    @action(detail=True, methods=['put'])
    def declined(self, request, pk, attributefilterset_pk):
        data = dict(status=Participation.STATUS.get_value('declined'))
        participation_serializer = self.get_serializer(data=data)
        participation_serializer.is_valid(raise_exception=True)
        participation_serializer.save()
        return Response(data=participation_serializer.data)

    @action(detail=True, methods=['put'])
    def recall(self, request, pk, attributefilterset_pk):
        data = request.data.copy()
        data['status'] = Participation.STATUS.get_value('pending')
        participation_serializer = self.get_serializer(data=data)
        participation_serializer.is_valid(raise_exception=True)
        participation_serializer.save()
        return Response(data=participation_serializer.data)

    @action(detail=True, methods=['put'])
    def participate(self, request, pk, attributefilterset_pk):
        data = request.data.copy()
        data['status'] = Participation.STATUS.get_value('accepted')
        participation_serializer = self.get_serializer(data=data)
        participation_serializer.is_valid(raise_exception=True)
        participation_serializer.save()
        return Response(data=participation_serializer.data)


class ContactHistoryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Subject.objects.all()
    serializer_class = ContactHistorySerializer

    def retrieve(self, request, pk=None):
        subject = self.get_object()
        contact_history = get_contact_history(subject)
        serializer = self.get_serializer(contact_history)
        return Response(serializer.data)
