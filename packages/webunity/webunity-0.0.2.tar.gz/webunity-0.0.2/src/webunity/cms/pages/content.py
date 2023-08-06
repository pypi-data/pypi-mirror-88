from wagtail.admin.edit_handlers import StreamFieldPanel

from webunity.bakery.abstract import BakeryMixin
from webunity.cms import constants
from webunity.loader import get_model
from webunity.cms.forms.abstract import FormMixin

GenericPage = get_model('cms', 'GenericPage')


class AContentPage(FormMixin, BakeryMixin, GenericPage):
    template = '%s/content_page.html' % constants.PAGES_TEMPLATES_PATH

    promote_panels = GenericPage.promote_panels + [
        StreamFieldPanel('schemas'),
    ]

    class Meta:
        abstract = True
        app_label = 'cms'
