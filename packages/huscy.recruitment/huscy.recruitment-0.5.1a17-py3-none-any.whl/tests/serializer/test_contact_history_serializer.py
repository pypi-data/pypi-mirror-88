import pytest
from model_bakery import baker

from huscy.recruitment.serializer import ContactHistorySerializer

pytestmark = pytest.mark.django_db


def test_serializer_contact_history_items(contact_history):
    baker.make('recruitment.ContactHistoryItem', contact_history=contact_history, _quantity=5)

    serializer = ContactHistorySerializer(contact_history)

    assert len(serializer.data['contact_history_items']) == 5
