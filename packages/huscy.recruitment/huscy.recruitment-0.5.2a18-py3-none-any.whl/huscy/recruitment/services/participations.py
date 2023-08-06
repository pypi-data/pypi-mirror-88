from datetime import timedelta

from django.contrib.contenttypes.models import ContentType

from huscy.appointments.services import create_appointment
from huscy.bookings.models import Timeslot
from huscy.bookings.services import book_timeslot
from huscy.pseudonyms.models import Pseudonym
from huscy.pseudonyms.services import get_or_create_pseudonym
from huscy.recruitment.models import Participation, Recall


def get_participations_for_project(project):
    return Participation.objects.filter(attribute_filterset__subject_group__project=project)


def create_or_update_participation(subject, attribute_filterset, status, **kwargs):
    content_type = ContentType.objects.get_by_natural_key('recruitment', 'participation')
    pseudonym = get_or_create_pseudonym(
        subject=subject,
        content_type=content_type,
        object_id=attribute_filterset.subject_group.project_id
    )

    participation, created = Participation.objects.get_or_create(
        pseudonym=pseudonym.code,
        attribute_filterset=attribute_filterset,
        defaults=dict(status=status),
    )

    if not created and not participation.status == status:
        participation.status = status
        participation.save(update_fields=['status'])

    if status == Participation.STATUS.get_value('pending') and 'appointment' in kwargs:
        creator = kwargs['user']
        start = kwargs['appointment']
        end = start + timedelta(minutes=30)

        try:
            recall = participation.recall.get()
            # TODO: create new appointment, if appointment.start is in the past
            recall.appointment.creator = creator
            recall.appointment.start = start
            recall.appointment.end = end
            recall.appointment.save()
        except Recall.DoesNotExist:
            appointment = create_appointment(creator=creator, start=start, end=end,
                                             title='recall appointment')
            Recall.objects.create(participation=participation, appointment=appointment)

    if status == Participation.STATUS.get_value('accepted'):
        timeslots = Timeslot.objects.filter(pk__in=kwargs['timeslots'])
        # TODO: add check, that timeslots belong to project
        for timeslot in timeslots:
            book_timeslot(timeslot=timeslot, subject=subject)

    return participation


def get_participations(subject=None, attribute_filterset=None):
    if attribute_filterset is None and subject is None:
        raise ValueError('Expected either attribute_filterset or subject args')

    pseudonyms = []
    if subject:
        content_type = ContentType.objects.get_by_natural_key('recruitment', 'participation')
        pseudonyms = (Pseudonym.objects.filter(subject=subject, content_type=content_type)
                                       .values_list('code', flat=True))
    if attribute_filterset and subject:
        return Participation.objects.filter(pseudonym__in=pseudonyms,
                                            attribute_filterset=attribute_filterset)
    elif attribute_filterset:
        return Participation.objects.filter(attribute_filterset=attribute_filterset)
    return Participation.objects.filter(pseudonym__in=pseudonyms)
