from itertools import cycle

import pytest
from model_bakery import baker

from huscy.pseudonyms.services import create_pseudonym
from huscy.recruitment.services.attribute_filtersets import _resolve_attributesets_to_subject_ids

pytestmark = pytest.mark.django_db


@pytest.fixture
def subjects():
    return baker.make('subjects.Subject', _quantity=3)


@pytest.fixture
def attribute_sets(subjects, attributeset_content_type):
    pseudonyms = [create_pseudonym(s, content_type=attributeset_content_type) for s in subjects]
    return baker.make('attributes.AttributeSet', attribute_schema__schema={},
                      pseudonym=cycle([pseudonym.code for pseudonym in pseudonyms]), _quantity=3)


def test_resolve_attributesets_to_subjects(attribute_sets, subjects):
    assert [subject.id for subject in subjects] == \
           list(_resolve_attributesets_to_subject_ids(attribute_sets))
