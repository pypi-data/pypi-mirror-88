import pytest

from model_bakery import baker


@pytest.mark.django_db
def test_default_status():
    participation = baker.make('recruitment.Participation')

    assert participation.status == 0
