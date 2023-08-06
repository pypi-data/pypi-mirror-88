import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_retrieve_participations(admin_client, project):
    response = retrieve_participations(admin_client, project)
    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_retrieve_participations(client, project):
    response = retrieve_participations(client, project)
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_anonymous_user_cannot_retrieve_participations(anonymous_client, project):
    response = retrieve_participations(anonymous_client, project)
    assert response.status_code == HTTP_403_FORBIDDEN


def retrieve_participations(client, project):
    return client.get(reverse('project-participations', kwargs=dict(pk=project.pk)))
