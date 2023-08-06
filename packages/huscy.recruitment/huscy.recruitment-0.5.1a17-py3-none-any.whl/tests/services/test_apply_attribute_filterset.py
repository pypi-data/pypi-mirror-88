from itertools import cycle

import pytest
from model_bakery import baker

from huscy.pseudonyms.services import create_pseudonym
from huscy.recruitment.services import apply_attribute_filterset

pytestmark = pytest.mark.django_db


@pytest.fixture
def subjects():
    return baker.make('subjects.Subject', _quantity=3)


@pytest.fixture
def attribute_schema():
    schema = {
        'type': 'object',
        'properties': {
            'handedness': {'type': 'string', 'enum': ['left', 'right']},
            'sex': {'type': 'string', 'enum': ['female', 'male']},
        },
    }
    return baker.make('attributes.AttributeSchema', schema=schema)


@pytest.fixture
def attribute_sets(attribute_schema, subjects, attributeset_content_type):
    pseudonyms = [create_pseudonym(s, content_type=attributeset_content_type) for s in subjects]

    attribute_sets = [
        {'handedness': 'right', 'sex': 'female'},
        {'handedness': 'left', 'sex': 'female'},
        {'handedness': 'right', 'sex': 'male'},
    ]

    return baker.make('attributes.AttributeSet', attribute_schema=attribute_schema,
                      pseudonym=cycle([pseudonym.code for pseudonym in pseudonyms]),
                      attributes=cycle(attribute_sets), _quantity=3)


def test_with_no_filters(attribute_sets, subjects):
    attribute_filterset = baker.make('recruitment.AttributeFilterSet', filters={})

    result = apply_attribute_filterset(attribute_filterset)

    assert list(result) == subjects


def test_with_two_filters(attribute_sets, subjects):
    filters = {'handedness': ['left'], 'sex': ['female']}
    attribute_filterset = baker.make('recruitment.AttributeFilterSet', filters=filters)

    result = apply_attribute_filterset(attribute_filterset)

    assert list(result) == [subjects[1]]
