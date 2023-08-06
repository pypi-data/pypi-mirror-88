from wagtail.core import blocks

from webunity.cms import constants
from webunity.cms.blocks.common import EntryBlock, EmbedWithSizeBlock


class EmbedEntry(EntryBlock):
    amp_scripts = ['iframe']
    animation = blocks.BooleanBlock(required=False, help_text="Animation")
    embed = EmbedWithSizeBlock()

    def mock(self, size_media='m', *args, **kwargs):
        self.mock_data.update({
            'type': 'embed',
            'value': {
                'embed': {
                    "link": self.URL_EMBED,
                    'size': size_media
                }
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/embed.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Embed"
        icon = 'media'
