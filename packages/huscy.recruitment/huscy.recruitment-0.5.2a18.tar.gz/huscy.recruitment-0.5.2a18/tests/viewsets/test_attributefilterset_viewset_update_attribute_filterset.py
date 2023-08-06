import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_update_attribute_filterset(admin_client, attribute_filterset):
    response = update_attribute_filterset(admin_client, attribute_filterset)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_update_attribute_filterset(client, attribute_filterset):
    response = update_attribute_filterset(client, attribute_filterset)

    assert response.status_code == HTTP_200_OK, response.json()


def test_anonymous_user_cannot_update_attribute_filterset(anonymous_client, attribute_filterset):
    response = update_attribute_filterset(anonymous_client, attribute_filterset)

    assert response.status_code == HTTP_403_FORBIDDEN


def update_attribute_filterset(client, attribute_filterset):
    return client.put(
        reverse('attributefilterset-detail', kwargs=dict(pk=attribute_filterset.pk)),
        data=dict(filters={'attribute': [[0, 10]]}),
        format='json'
    )
