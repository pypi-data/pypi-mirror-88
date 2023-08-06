from datetime import datetime

import pytest

from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.appointments.models import Appointment
from huscy.pseudonyms.services import get_pseudonym
from huscy.recruitment.models import Participation

pytestmark = pytest.mark.django_db


def test_admin_user_can_set_recall(admin_client, attribute_filterset, subject):
    response = recall(admin_client, attribute_filterset, subject)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_set_recall(client, attribute_filterset, subject):
    response = recall(client, attribute_filterset, subject)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_set_recall(anonymous_client, attribute_filterset, subject):
    response = recall(anonymous_client, attribute_filterset, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_initial_contact_attempt_creates_participation(client, attribute_filterset, subject):
    assert not Participation.objects.exists()

    recall(client, attribute_filterset, subject)

    content_type = ContentType.objects.get_by_natural_key('recruitment', 'participation')
    pseudonym = get_pseudonym(subject, content_type, attribute_filterset.subject_group.project_id)

    participation = Participation.objects.get()
    assert participation.pseudonym == pseudonym.code
    assert participation.attribute_filterset == attribute_filterset
    assert participation.status == Participation.STATUS.get_value('pending')


def test_keep_status_pending(client, participation, subject):
    assert 1 == Participation.objects.count()

    recall(client, participation.attribute_filterset, subject)

    participation = Participation.objects.get()
    assert participation.status == Participation.STATUS.get_value('pending')


def test_create_recall_appointment(client, user, attribute_filterset, subject):
    assert not Appointment.objects.exists()

    recall(client, attribute_filterset, subject, appointment=datetime(2020, 1, 1, 14, 30))

    appointment = Appointment.objects.get()
    assert appointment.owner == user
    assert appointment.start == datetime(2020, 1, 1, 14, 30)
    assert appointment.end == datetime(2020, 1, 1, 15)
    assert appointment.title == 'recall appointment'


def recall(client, attribute_filterset, subject, appointment=None):
    return client.put(
        reverse(
            'participation-recall',
            kwargs=dict(pk=str(subject.pk), attributefilterset_pk=attribute_filterset.pk)
        ),
        data=None if appointment is None else dict(appointment=appointment),
    )
