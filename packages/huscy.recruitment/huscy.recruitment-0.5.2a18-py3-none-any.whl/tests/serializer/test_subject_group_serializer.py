import pytest

from huscy.recruitment.serializer import AttributeFilterSetSerializer, SubjectGroupSerializer

pytestmark = pytest.mark.django_db


def test_expose_attribute_filtersets(attribute_filterset):
    data = SubjectGroupSerializer(attribute_filterset.subject_group).data

    assert len(data['attribute_filtersets']) == 1

    attribute_filterset_serializer = AttributeFilterSetSerializer([attribute_filterset], many=True)
    assert data['attribute_filtersets'] == attribute_filterset_serializer.data


def test_attribute_filtersets_are_read_only(attribute_filterset):
    subject_group = dict(
        attribute_filtersets=AttributeFilterSetSerializer([attribute_filterset], many=True).data,
        description='description',
        name='name',
        project=attribute_filterset.subject_group.project.pk,
    )
    subject_group_serializer = SubjectGroupSerializer(data=subject_group)
    subject_group_serializer.is_valid()
    assert 'attribute_filtersets' not in subject_group_serializer.validated_data
