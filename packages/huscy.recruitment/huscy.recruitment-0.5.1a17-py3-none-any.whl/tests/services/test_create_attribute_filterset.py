import pytest

from huscy.recruitment.services import create_attribute_filterset


@pytest.mark.django_db
def test_create_attribute_filterset(subject_group):
    filterset = create_attribute_filterset(subject_group)

    assert filterset.subject_group == subject_group
    assert filterset.filters == {}
