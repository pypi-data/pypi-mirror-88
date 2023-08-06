import operator
from functools import reduce

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from huscy.attributes.models import AttributeSet
from huscy.attributes.services import get_attribute_schema
from huscy.pseudonyms.services import get_subject
from huscy.recruitment.models import AttributeFilterSet
from huscy.subjects.models import Subject


def create_attribute_filterset(subject_group):
    return AttributeFilterSet.objects.create(subject_group=subject_group)


def update_attribute_filterset(attribute_filterset, filters):
    attribute_filterset.filters = filters
    attribute_filterset.save()
    return attribute_filterset


def apply_attribute_filterset(attribute_filterset):
    attribute_sets = _filter_attributesets_by_filterset(attribute_filterset)
    subject_ids = _resolve_attributesets_to_subject_ids(attribute_sets)
    return Subject.objects.filter(id__in=subject_ids)


def _filter_attributesets_by_filterset(attribute_filterset):
    filters = _get_filters(attribute_filterset)
    return AttributeSet.objects.filter(*filters)


def _get_filters(attribute_filterset):
    attribute_schema = get_attribute_schema()

    for attribute_name, filter_values in attribute_filterset.filters.items():
        exclude = False

        if attribute_name.startswith('-'):
            attribute_name = attribute_name[1:]
            exclude = True

        attribute_type = _get_attribute_type(attribute_schema.schema, attribute_name)

        if attribute_type in ['integer', 'number']:
            lookup = f'attributes__{attribute_name}__range'
        elif attribute_type == 'array':
            lookup = f'attributes__{attribute_name}__contains'
        else:
            lookup = f'attributes__{attribute_name}'

        q = reduce(operator.or_, (Q(**{lookup: filter_value}) for filter_value in filter_values))

        if exclude:
            q = ~Q(q)

        yield q


def _get_attribute_type(schema, attribute_name):
    path = ['properties'] + attribute_name.replace('__', '__properties__').split('__')
    attribute = reduce(operator.getitem, path, schema)
    return attribute['type']


def _resolve_attributesets_to_subject_ids(attribute_sets):
    content_type = ContentType.objects.get(app_label='attributes', model='attributeset')
    for attribute_set in attribute_sets:
        yield get_subject(attribute_set.pseudonym, content_type).pk
