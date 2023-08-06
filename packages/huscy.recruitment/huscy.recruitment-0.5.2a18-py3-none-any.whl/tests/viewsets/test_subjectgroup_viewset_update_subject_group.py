import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_update_subject_group(admin_client, subject_group):
    response = update_subject_group(admin_client, subject_group)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_update_subject_group(client, subject_group):
    response = update_subject_group(client, subject_group)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_update_subject_group(anonymous_client, subject_group):
    response = update_subject_group(anonymous_client, subject_group)

    assert response.status_code == HTTP_403_FORBIDDEN


def update_subject_group(client, subject_group):
    project = subject_group.project
    return client.put(
        reverse('subjectgroup-detail', kwargs=dict(project_pk=project.pk, pk=subject_group.pk)),
        data=dict(
            description=subject_group.description,
            name=subject_group.name,
            order=subject_group.order,
        )
    )
