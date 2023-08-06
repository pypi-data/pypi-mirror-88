from datetime import datetime, timedelta

import pytest
from model_bakery import baker

from django.contrib.contenttypes.models import ContentType

from rest_framework.test import APIClient


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='user', password='password',
                                                 first_name='Clara', last_name='Himmel')


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.login(username=admin_user.username, password='password')
    return client


@pytest.fixture
def client(user):
    client = APIClient()
    client.login(username=user.username, password='password')
    return client


@pytest.fixture
def anonymous_client():
    return APIClient()


@pytest.fixture
def content_type_contact_history():
    return ContentType.objects.get(app_label='recruitment', model='contacthistory')


@pytest.fixture
def attribute_schema(django_db_reset_sequences):
    schema = {
        'type': 'object',
        'properties': {
            'attribute': {'type': 'number'}
        },
    }
    return baker.make('attributes.AttributeSchema', schema=schema)


@pytest.fixture
def subject():
    return baker.make('subjects.Subject')


@pytest.fixture
def project():
    return baker.make('projects.Project')


@pytest.fixture
def subject_group(project):
    return baker.make('recruitment.SubjectGroup', project=project)


@pytest.fixture
def attribute_filterset(subject_group):
    return baker.make('recruitment.AttributeFilterSet', subject_group=subject_group)


@pytest.fixture
def attributeset_content_type():
    return ContentType.objects.get(app_label='attributes', model='attributeset')


@pytest.fixture
def participation_content_type():
    return ContentType.objects.get(app_label='recruitment', model='participation')


@pytest.fixture
def participation_pseudonym(subject, attribute_filterset, participation_content_type):
    return baker.make('pseudonyms.Pseudonym', subject=subject,
                      content_type=participation_content_type,
                      object_id=attribute_filterset.subject_group.project_id)


@pytest.fixture
def participation(subject, attribute_filterset, participation_pseudonym):
    return baker.make('recruitment.Participation', attribute_filterset=attribute_filterset,
                      pseudonym=participation_pseudonym.code)


@pytest.fixture
def contact_history(subject, content_type_contact_history):
    pseudonym = baker.make('pseudonyms.Pseudonym', subject=subject,
                           content_type=content_type_contact_history)
    return baker.make('recruitment.ContactHistory', pseudonym=pseudonym.code)


@pytest.fixture
def session(project):
    return baker.make('projects.Session', experiment__project=project, duration=timedelta(hours=1))


@pytest.fixture
def timeslot(session):
    baker.make('appointments.Resource', name='a111')
    baker.make('projects.DataAcquisitionMethod', session=session, location='a111')
    return baker.make('bookings.Timeslot', session=session, active=True,
                      start=datetime(2020, 1, 1, 10))
