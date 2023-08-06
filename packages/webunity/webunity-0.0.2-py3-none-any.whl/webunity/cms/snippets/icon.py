from django.db import models
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel

from wagtailsvg.models import Svg
from wagtailsvg.edit_handlers import SvgChooserPanel
from webunity.loader import get_model


class AIconSnippet(index.Indexed, models.Model):
    DEFAULT_LINK = '/static/webunity/img/svg/default.svg'
    key = models.CharField(max_length=255)
    light = models.ForeignKey(
        Svg,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Theme Secondary"
    )
    space = models.ForeignKey(
        Svg,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Theme Primary"
    )

    panels = [
        FieldPanel('key'),
        SvgChooserPanel('space'),
        SvgChooserPanel('light'),
    ]

    search_fields = [
        index.SearchField('key', partial_match=True),
    ]

    def __str__(self):
        return self.key

    @staticmethod
    def get_context():
        IconSnippet = get_model('cms', 'IconSnippet')
        ret = {}
        for icon in IconSnippet.objects.all():
            ret[icon.key] = {
                'space': icon.space.url if icon.space else IconSnippet.DEFAULT_LINK,
                'light': icon.light.url if icon.light else IconSnippet.DEFAULT_LINK,
            }
        return ret

    class Meta:
        verbose_name = "Icon"
        abstract = True
        app_label = 'cms'
