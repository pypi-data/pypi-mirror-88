import pytest
from model_bakery import baker

from huscy.recruitment.services import get_subject_groups

pytestmark = pytest.mark.django_db


def test_with_no_groups(project):
    result = get_subject_groups(project)

    assert [] == list(result)


def test_with_one_group(project):
    subject_group = baker.make('recruitment.SubjectGroup', project=project)

    result = get_subject_groups(project)

    assert [subject_group] == list(result)


def test_with_multiple_groups(project):
    def sort_function(item):
        return getattr(item, 'id')

    subject_groups = baker.make('recruitment.SubjectGroup', project=project, _quantity=3)

    result = get_subject_groups(project)

    assert sorted(subject_groups, key=sort_function) == sorted(result, key=sort_function)
