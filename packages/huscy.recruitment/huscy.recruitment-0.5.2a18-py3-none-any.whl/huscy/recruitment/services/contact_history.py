from django.contrib.contenttypes.models import ContentType

from huscy.pseudonyms.services import get_or_create_pseudonym
from huscy.recruitment.models import ContactHistory


def get_contact_history(subject):
    content_type = ContentType.objects.get_by_natural_key('recruitment', 'contacthistory')
    pseudonym = get_or_create_pseudonym(subject, content_type)

    contact_history, _created = ContactHistory.objects.get_or_create(pseudonym=pseudonym.code)
    return contact_history
