import pytest

from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.pseudonyms.services import get_pseudonym
from huscy.recruitment.models import Participation

pytestmark = pytest.mark.django_db


def test_admin_user_can_set_not_reached(admin_client, attribute_filterset, subject):
    response = not_reached(admin_client, attribute_filterset, subject)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_set_not_reached(client, attribute_filterset, subject):
    response = not_reached(client, attribute_filterset, subject)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_set_not_reached(anonymous_client, attribute_filterset, subject):
    response = not_reached(anonymous_client, attribute_filterset, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_initial_contact_attempt_creates_participation(client, attribute_filterset, subject):
    assert not Participation.objects.exists()

    not_reached(client, attribute_filterset, subject)

    content_type = ContentType.objects.get_by_natural_key('recruitment', 'participation')
    pseudonym = get_pseudonym(subject, content_type, attribute_filterset.subject_group.project_id)

    participation = Participation.objects.get()
    assert participation.pseudonym == pseudonym.code
    assert participation.attribute_filterset == attribute_filterset
    assert participation.status == Participation.STATUS.get_value('pending')


def test_status_unchanged_onsecond_contact_attempt(client, participation, subject):
    assert 1 == Participation.objects.count()

    not_reached(client, participation.attribute_filterset, subject)

    participation = Participation.objects.get()
    assert participation.status == Participation.STATUS.get_value('pending')


def not_reached(client, attribute_filterset, subject):
    return client.put(
        reverse('participation-not-reached',
                kwargs=dict(pk=str(subject.pk), attributefilterset_pk=attribute_filterset.pk))
    )
