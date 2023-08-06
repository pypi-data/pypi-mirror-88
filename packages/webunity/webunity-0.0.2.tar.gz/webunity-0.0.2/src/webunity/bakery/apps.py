import fs
from django.apps import AppConfig
from wagtail.core.signals import page_published


def handle_publish(sender, instance, **kwargs):
    from .abstract import BakeryMixin
    if isinstance(instance, BakeryMixin):
        instance.build()


class BakeryConfig(AppConfig):
    name = 'webunity.bakery'
    label = 'bakery'
    verbose_name = 'bakery'
    filesystem_name = "osfs:///"
    filesystem = fs.open_fs(filesystem_name)

    def ready(self):
        page_published.connect(
            handle_publish,
            dispatch_uid='wagtailbakery_page_published'
        )
