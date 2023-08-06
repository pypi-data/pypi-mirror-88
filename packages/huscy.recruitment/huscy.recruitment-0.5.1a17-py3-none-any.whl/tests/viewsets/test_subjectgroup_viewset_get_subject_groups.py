import pytest
from model_bakery import baker

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.recruitment.models import SubjectGroup

pytestmark = pytest.mark.django_db


def test_admin_user_can_list_subject_groups(admin_client, project):
    response = list_subject_groups(admin_client, project)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_list_subject_groups(client, project):
    response = list_subject_groups(client, project)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_list_subject_groups(anonymous_client, project):
    response = list_subject_groups(anonymous_client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_create_subject_group_when_project_has_no_subject_groups(client, project):
    assert SubjectGroup.objects.count() == 0

    list_subject_groups(client, project)

    assert SubjectGroup.objects.count() == 1


def test_dont_create_new_subject_group_when_project_already_has_some(client, project):
    baker.make('recruitment.SubjectGroup', project=project, _quantity=2)

    assert SubjectGroup.objects.count() == 2

    list_subject_groups(client, project)

    assert SubjectGroup.objects.count() == 2


def list_subject_groups(client, project):
    return client.get(reverse('subjectgroup-list', kwargs=dict(project_pk=project.pk)))
