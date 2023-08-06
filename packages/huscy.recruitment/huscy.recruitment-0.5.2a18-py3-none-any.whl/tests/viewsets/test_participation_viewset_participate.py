import pytest

from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.pseudonyms.services import get_pseudonym
from huscy.recruitment.models import Participation

pytestmark = pytest.mark.django_db


def test_admin_user_can_set_participate(admin_client, attribute_filterset, subject, timeslot):
    response = participate(admin_client, attribute_filterset, subject, timeslot)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_set_participate(client, attribute_filterset, subject,
                                                     timeslot):
    response = participate(client, attribute_filterset, subject, timeslot)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_set_participate(anonymous_client, attribute_filterset, subject,
                                               timeslot):
    response = participate(anonymous_client, attribute_filterset, subject, timeslot)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_initial_contact_attempt_creates_participation(client, attribute_filterset, subject,
                                                       timeslot):
    assert not Participation.objects.exists()

    participate(client, attribute_filterset, subject, timeslot)

    content_type = ContentType.objects.get_by_natural_key('recruitment', 'participation')
    pseudonym = get_pseudonym(subject, content_type, attribute_filterset.subject_group.project_id)

    participation = Participation.objects.get()
    assert participation.pseudonym == pseudonym.code
    assert participation.attribute_filterset == attribute_filterset
    assert participation.status == Participation.STATUS.get_value('accepted')


def test_set_status_accepted(client, participation, subject, timeslot):
    assert 1 == Participation.objects.count()

    participate(client, participation.attribute_filterset, subject, timeslot)

    participation = Participation.objects.get()
    assert participation.status == Participation.STATUS.get_value('accepted')


def test_book_timeslots(client, user, attribute_filterset, subject, timeslot):
    assert timeslot.active is True
    assert not timeslot.booking_set.exists()

    participate(client, attribute_filterset, subject, timeslot)

    timeslot.refresh_from_db()
    assert timeslot.active is False
    assert timeslot.booking_set.count() == 1


def participate(client, attribute_filterset, subject, timeslot):
    return client.put(
        reverse(
            'participation-participate',
            kwargs=dict(pk=str(subject.pk), attributefilterset_pk=attribute_filterset.pk)
        ),
        data=dict(timeslots=[timeslot.pk]),
    )
