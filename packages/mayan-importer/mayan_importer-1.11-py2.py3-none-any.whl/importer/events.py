from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Importer'), name='importer')

event_import_setup_created = namespace.add_event_type(
    label=_('Import setup created'), name='import_setup_created'
)
event_import_setup_edited = namespace.add_event_type(
    label=_('Import setup edited'), name='import_setup_edited'
)
event_import_setup_processed = namespace.add_event_type(
    label=_('Import setup processed'), name='import_setup_processed'
)
event_import_setup_item_completed = namespace.add_event_type(
    label=_('Import setup item completed'), name='import_setup_item_completed'
)
