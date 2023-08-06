import pytest
from model_bakery import baker

pytestmark = pytest.mark.django_db


def test_delete_project(project):
    contact_history_item = baker.make('recruitment.ContactHistoryItem', project=project)

    project.delete()
    contact_history_item.refresh_from_db()

    assert contact_history_item.project is None
