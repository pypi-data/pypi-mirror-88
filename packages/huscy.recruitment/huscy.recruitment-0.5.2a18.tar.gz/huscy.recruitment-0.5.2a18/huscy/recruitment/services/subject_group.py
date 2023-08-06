from django.db.models import F

from huscy.recruitment.models import SubjectGroup
from huscy.recruitment.services.attribute_filtersets import create_attribute_filterset


def create_subject_group(project, name, description):
    subject_group = SubjectGroup.objects.create(
        project=project,
        name=name,
        description=description,
        order=SubjectGroup.objects.filter(project=project).count(),
    )
    create_attribute_filterset(subject_group)
    return subject_group


def delete_subject_group(subject_group):
    if subject_group.project.subject_groups.count() == 1:
        raise ValueError('Cannot delete subject group. At least one subject group must remain for '
                         'the project.')

    (SubjectGroup.objects.filter(project=subject_group.project, order__gt=subject_group.order)
                         .update(order=F('order') - 1))
    subject_group.delete()


def get_subject_groups(project):
    return project.subject_groups.all()
