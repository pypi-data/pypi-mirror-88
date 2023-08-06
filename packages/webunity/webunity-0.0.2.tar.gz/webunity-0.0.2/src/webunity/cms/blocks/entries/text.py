from webunity.cms.blocks.choice import AlignTextChoiceBlock
from webunity.cms import constants
from webunity.cms.blocks.common import \
    TextBlock, \
    EntryBlock


class TextEntry(EntryBlock):
    align = AlignTextChoiceBlock(required=False, default=constants.ALIGN_TEXT_LEFT)
    text = TextBlock()

    def mock(self, txt=None, size='big', align=None, *args, **kwargs):
        self.mock_data.update({
            'type': 'text',
            'value': {
                'text': {
                    'value': txt if txt else eval('self.' + size),
                },
                'align': align
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Text"
        icon = 'edit'
