import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.recruitment import models

pytestmark = pytest.mark.django_db


def test_admin_user_can_create_subject_group(admin_client, project):
    response = create_subject_group(admin_client, project)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_can_create_subject_group(client, project):
    response = create_subject_group(client, project)

    assert response.status_code == HTTP_201_CREATED


def test_anonymous_user_cannot_create_subject_group(anonymous_client, project):
    response = create_subject_group(anonymous_client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_attribute_filterset_created(client, project):
    assert not models.SubjectGroup.objects.exists()
    assert not models.AttributeFilterSet.objects.exists()

    create_subject_group(client, project)

    assert models.SubjectGroup.objects.exists()
    assert models.AttributeFilterSet.objects.exists()


def create_subject_group(client, project):
    return client.post(
        reverse('subjectgroup-list', kwargs=dict(project_pk=project.pk)),
        data=dict(
            description='description',
            name='name',
        )
    )
