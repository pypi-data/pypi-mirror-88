from wagtail.core import blocks

from webunity.cms import constants
from webunity.cms.blocks.choice import AlignTextChoiceBlock
from webunity.cms.blocks.common import ButtonsBlock, EntryBlock


class ButtonsEntry(EntryBlock):
    align = AlignTextChoiceBlock(required=False, default=constants.ALIGN_TEXT_LEFT)
    buttons = ButtonsBlock()

    def mock(self, btn_one=constants.BUTTON_SECONDARY_FULL, btn_two=constants.BUTTON_SECONDARY, align='left',
             *args, **kwargs):
        self.mock_data.update({
            'type': 'buttons',
            'value': {
                'buttons': [
                    {
                        'type': 'button',
                        'value': self.button(btn_one)
                    },
                    {
                        'type': 'button',
                        'value': self.button(btn_two)
                    },
                ],
                'align': align
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/buttons.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Buttons"
        icon = 'link'
