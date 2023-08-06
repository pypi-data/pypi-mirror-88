from huscy.recruitment.models import ContactHistoryItem
from huscy.recruitment.services.participations import get_participations


def get_contact_history_items(participation):
    return ContactHistoryItem.objects.filter(participation=participation).order_by('created_at')


def get_contact_history_items_by_subject(subject, project=None):
    participations = get_participations(subject=subject)

    if project:
        participations = participations.filter(project=project)

    return (ContactHistoryItem.objects.filter(participation__in=participations)
                                      .order_by('created_at'))


def create_contact_history_item(participation, status=0):
    return ContactHistoryItem.objects.create(participation=participation, status=status)
