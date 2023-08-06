import pytest
from model_bakery import baker

from huscy.recruitment.serializer import ContactHistoryItemSerializer

pytestmark = pytest.mark.django_db


def test_project_title_with_project():
    contact_history_item = baker.make('recruitment.ContactHistoryItem',
                                      project__title='Exciting project')

    serializer_data = ContactHistoryItemSerializer(contact_history_item).data

    assert serializer_data['project_title'] == 'Exciting project'


def test_project_title_without_project():
    contact_history_item = baker.make('recruitment.ContactHistoryItem')

    serializer_data = ContactHistoryItemSerializer(contact_history_item).data

    assert serializer_data['project_title'] == 'Deleted project'
