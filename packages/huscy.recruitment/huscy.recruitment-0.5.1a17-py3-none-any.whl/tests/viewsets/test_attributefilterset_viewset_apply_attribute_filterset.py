import pytest
from model_bakery import baker

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.attributes.services import get_or_create_attribute_set

pytestmark = pytest.mark.django_db


@pytest.fixture
def subjects():
    return baker.make('subjects.Subject', _quantity=5)


@pytest.fixture
def attribute_sets(attribute_schema, subjects):
    return list(map(get_or_create_attribute_set, subjects))


def test_admin_user_can_apply_attribute_filterset(admin_client, attribute_filterset):
    response = apply_attribute_filterset(admin_client, attribute_filterset)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_apply_attribute_filterset(client, attribute_filterset):
    response = apply_attribute_filterset(client, attribute_filterset)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_apply_attribute_filterset(anonymous_client, attribute_filterset):
    response = apply_attribute_filterset(anonymous_client, attribute_filterset)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_filter_subjects_with_initial_attribute_sets(client, attribute_filterset, attribute_sets):
    response = apply_attribute_filterset(client, attribute_filterset)

    assert len(response.json()) == 5


def test_filter_subjects_with_empty_filterset(client, attribute_filterset, attribute_sets):
    for count, attribute_set in enumerate(attribute_sets):
        attribute_set.attributes['attribute'] = attribute_set.id
        attribute_set.save()

    response = apply_attribute_filterset(client, attribute_filterset)

    assert len(response.json()) == 5


def test_filter_subjects(client, subject_group, subjects, attribute_sets):
    for count, attribute_set in enumerate(attribute_sets):
        attribute_set.attributes['attribute'] = attribute_set.id
        attribute_set.save()

    attribute_filterset = baker.make('recruitment.AttributeFilterSet', subject_group=subject_group,
                                     filters={'attribute': [[3, 4]]})

    response = apply_attribute_filterset(client, attribute_filterset)

    results = response.json()
    assert len(results) == 2
    assert results[0]['id'] == str(subjects[2].id)
    assert results[1]['id'] == str(subjects[3].id)


def apply_attribute_filterset(client, attribute_filterset):
    return client.get(reverse('attributefilterset-apply', kwargs=dict(pk=attribute_filterset.pk)))
