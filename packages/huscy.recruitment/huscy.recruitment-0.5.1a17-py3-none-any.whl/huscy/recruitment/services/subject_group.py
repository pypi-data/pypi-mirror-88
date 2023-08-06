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


def get_subject_groups(project):
    return project.subject_groups.all()
