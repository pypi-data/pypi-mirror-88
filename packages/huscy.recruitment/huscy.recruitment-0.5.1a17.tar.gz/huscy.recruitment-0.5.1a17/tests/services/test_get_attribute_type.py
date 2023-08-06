import pytest

from huscy.recruitment.services.attribute_filtersets import _get_attribute_type


@pytest.fixture
def schema():
    return {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'integer'},
            'attribute2': {
                'type': 'object',
                'properties': {
                    'attribute21': {
                        'type': 'object',
                        'properties': {
                            'attribute211': {'type': 'string'},
                        },
                    },
                },
            },
        },
    }


@pytest.mark.parametrize('attribute,expected', [
    ('attribute1', 'integer'),
    ('attribute2__attribute21', 'object'),
    ('attribute2__attribute21__attribute211', 'string'),
])
def test_get_attribute_type_from_flat_structure(schema, attribute, expected):
    assert expected == _get_attribute_type(schema, attribute)
