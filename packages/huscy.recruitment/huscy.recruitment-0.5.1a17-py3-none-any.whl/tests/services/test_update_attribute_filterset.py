import pytest

from huscy.recruitment.services import update_attribute_filterset

pytestmark = pytest.mark.django_db


def test_update_attribute_filterset(attribute_filterset):
    result = update_attribute_filterset(attribute_filterset, {'attribute1': 5})

    attribute_filterset.refresh_from_db()
    assert attribute_filterset == result
    assert attribute_filterset.filters == {'attribute1': 5}
