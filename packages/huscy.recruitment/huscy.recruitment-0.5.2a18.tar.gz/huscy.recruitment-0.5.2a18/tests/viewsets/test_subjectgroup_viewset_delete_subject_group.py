import pytest
from model_bakery import baker

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_delete_subject_group(admin_client, project):
    subject_groups = baker.make('recruitment.SubjectGroup', project=project, _quantity=2)

    response = delete_subject_group(admin_client, subject_groups[1])

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_can_delete_subject_group(client, project):
    subject_groups = baker.make('recruitment.SubjectGroup', project=project, _quantity=2)

    response = delete_subject_group(client, subject_groups[1])

    assert response.status_code == HTTP_204_NO_CONTENT


def test_anonymous_user_cannot_delete_subject_group(anonymous_client, project):
    subject_groups = baker.make('recruitment.SubjectGroup', project=project, _quantity=2)

    response = delete_subject_group(anonymous_client, subject_groups[1])

    assert response.status_code == HTTP_403_FORBIDDEN


def delete_subject_group(client, subject_group):
    project = subject_group.project

    return client.delete(
        reverse('subjectgroup-detail', kwargs=dict(project_pk=project.pk, pk=subject_group.pk))
    )
