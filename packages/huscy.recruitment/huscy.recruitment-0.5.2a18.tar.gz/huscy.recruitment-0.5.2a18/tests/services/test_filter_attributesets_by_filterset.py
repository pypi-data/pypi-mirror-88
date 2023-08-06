from itertools import cycle

import pytest
from model_bakery import baker

from huscy.recruitment.services.attribute_filtersets import _filter_attributesets_by_filterset

pytestmark = pytest.mark.django_db


@pytest.fixture
def attribute_schema():
    schema = {
        'type': 'object',
        'properties': {
            'handedness': {
                'type': 'string',
                'enum': ['left', 'right'],
            },
            'sex': {
                'type': 'string',
                'enum': ['female', 'male'],
            },
            'weight': {
                'type': 'integer',
            },
            'visual acuity': {
                'type': 'number',
            },
            'languages': {
                'type': 'array',
            },
            'nested': {
                'type': 'object',
                'properties': {
                    'nested_attribute': {
                        'type': 'integer',
                    }
                }
            },
        },
    }
    return baker.make('attributes.AttributeSchema', schema=schema)


@pytest.fixture
def attribute_sets(attribute_schema):
    attributes = [
        {
            'handedness': 'right',
            'sex': 'female',
            'weight': 55,
            'visual acuity': 0,
            'languages': ['German'],
            'nested': {'nested_attribute': 10},
        },
        {
            'handedness': 'left',
            'sex': 'female',
            'weight': 60,
            'visual acuity': -0.25,
            'languages': ['German', 'English'],
            'nested': {'nested_attribute': 50},
        },
        {
            'handedness': 'right',
            'sex': 'male',
            'weight': 75,
            'visual acuity': 1.5,
            'languages': ['English'],
            'nested': {'nested_attribute': 100},
        },
    ]
    return baker.make('attributes.AttributeSet', pseudonym=cycle(['p1', 'p2', 'p3']),
                      attributes=cycle(attributes), attribute_schema=attribute_schema, _quantity=3)


@pytest.mark.parametrize('filters,expected_pseudonyms', [
    ({}, ['p1', 'p2', 'p3']),  # test empty filterset
    ({'handedness': ['right']}, ['p1', 'p3']),  # test with one choice
    ({'handedness': ['right'], 'sex': ['female']}, ['p1']),  # test with multiple filters
    ({'weight': [[60, 75]]}, ['p2', 'p3']),  # test with integer filter
    ({'visual acuity': [[-0.5, 0.5]]}, ['p1', 'p2']),  # test with number filter

    ({'languages': [['German']]}, ['p1', 'p2']),  # test with single array element
    ({'languages': [['English']]}, ['p2', 'p3']),  # test with another single array element
    ({'languages': [['German', 'English']]}, ['p2']),  # test with multiple array elements
    ({'languages': [['English', 'German']]}, ['p2']),  # test with multiple array elements (mixed)

    ({'nested__nested_attribute': [[0, 50]]}, ['p1', 'p2']),

    ({'-handedness': ['left']}, ['p1', 'p3']),  # test with enum exclusion
    ({'-weight': [[50, 70]]}, ['p3']),  # test with integer exclusion
    ({'-languages': [['German']]}, ['p3']),  # test with arrey element exclusion

    ({'handedness': ['left', 'right']}, ['p1', 'p2', 'p3']),  # test enum with or condition
    ({'weight': [[50, 55], [70, 80]]}, ['p1', 'p3']),  # test integer with or condition
    ({'languages': [['English'], ['German']]}, ['p1', 'p2', 'p3']),  # test array with or condition
    ({'-weight': [[50, 55], [70, 80]]}, ['p2']),  # test exclusion with or condition
])
def test_filter_attributesets_by_filterset(attribute_sets, filters, expected_pseudonyms):
    attribute_filterset = baker.make('recruitment.AttributeFilterSet', filters=filters)

    result = _filter_attributesets_by_filterset(attribute_filterset)

    assert list(result.values_list('pseudonym', flat=True)) == expected_pseudonyms
