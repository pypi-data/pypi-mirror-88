from enum import Enum

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from django.utils.translation import gettext_lazy as _

from huscy.appointments.models import Appointment
from huscy.projects.models import Project


class SubjectGroup(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='subject_groups')
    name = models.CharField(max_length=126)
    description = models.TextField(blank=True, default='')
    order = models.PositiveSmallIntegerField(blank=True, default=0)


class AttributeFilterSet(models.Model):
    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE,
                                      related_name='attribute_filtersets')
    filters = JSONField(default=dict)


class Participation(models.Model):
    class STATUS(Enum):
        pending = (0, _('Pending'))
        declined = (1, _('Declined'))
        accepted = (2, _('Accepted'))
        in_progress = (3, _('In progress'))
        canceled = (4, _('Canceled'))
        finished = (5, _('Finished'))

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    attribute_filterset = models.ForeignKey(AttributeFilterSet, on_delete=models.PROTECT,
                                            related_name='participations')

    pseudonym = models.CharField(max_length=255, verbose_name=_('Pseudonym'), unique=True)
    status = models.PositiveSmallIntegerField(choices=[x.value for x in STATUS],
                                              default=STATUS.get_value('pending'),
                                              verbose_name=_('Status'))

    created_at = models.DateTimeField(auto_now_add=True)


class Recall(models.Model):
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE,
                                      related_name='recall')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)


class ContactHistory(models.Model):
    pseudonym = models.CharField(primary_key=True, editable=False, max_length=64)


class ContactHistoryItem(models.Model):
    class STATUS(Enum):
        not_reached = (0, _('Not reached'))
        recall = (1, _('Recall'))
        invited = (2, _('Invited'))

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    contact_history = models.ForeignKey(ContactHistory, on_delete=models.CASCADE,
                                        related_name='contact_history_items')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    status = models.PositiveSmallIntegerField(choices=[x.value for x in STATUS],
                                              default=STATUS.get_value('not_reached'),
                                              verbose_name=_('Status'))

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
