import pytest

from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.pseudonyms.services import get_pseudonym
from huscy.recruitment.models import ContactHistory

pytestmark = pytest.mark.django_db


def test_admin_user_can_retrieve_contact_history(admin_client, subject):
    response = retrieve_contact_history(admin_client, subject)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_retrieve_contact_history(client, subject):
    response = retrieve_contact_history(client, subject)

    assert response.status_code == HTTP_200_OK, response.json()


def test_anonymous_user_cannot_retrieve_contact_history(anonymous_client, subject):
    response = retrieve_contact_history(anonymous_client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_create_contact_history_if_it_does_not_exist(client, subject):
    assert not ContactHistory.objects.exists()

    retrieve_contact_history(client, subject)

    content_type = ContentType.objects.get_by_natural_key('recruitment', 'contacthistory')
    pseudonym = get_pseudonym(subject, content_type)
    assert ContactHistory.objects.filter(pseudonym=pseudonym.code).exists()


def retrieve_contact_history(client, subject):
    return client.get(reverse('contacthistory-detail', kwargs=dict(pk=subject.pk)))
