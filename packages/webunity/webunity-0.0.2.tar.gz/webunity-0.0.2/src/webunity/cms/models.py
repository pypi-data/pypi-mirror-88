from wagtail.contrib.settings.models import register_setting
from wagtail.snippets.models import register_snippet
from wagtail.core.models import TranslatableMixin

from webunity.loader import is_model_registered

__all__ = []

# Snippets

from .snippets.icon import AIconSnippet

if not is_model_registered('cms', 'IconSnippet'):
    @register_snippet
    class IconSnippet(AIconSnippet):
        pass


    __all__.append('IconSnippet')

from .snippets.menu import AMenu, AMenuItem

if not is_model_registered('cms', 'Menu'):
    @register_snippet
    class Menu(TranslatableMixin, AMenu):
        pass


    __all__.append('Menu')

if not is_model_registered('cms', 'MenuItem'):
    class MenuItem(TranslatableMixin, AMenuItem):
        pass


    __all__.append('MenuItem')

from .snippets.navigation import ANavigation

if not is_model_registered('cms', 'Navigation'):
    @register_snippet
    class Navigation(TranslatableMixin, ANavigation):
        pass


    __all__.append('Navigation')

from .snippets.form import AForm, AFormField, AFormSubmission

if not is_model_registered('cms', 'Form'):
    @register_snippet
    class Form(TranslatableMixin, AForm):
        pass


    __all__.append('Form')

if not is_model_registered('cms', 'FormField'):
    class FormField(AFormField):
        pass


    __all__.append('FormField')

if not is_model_registered('cms', 'FormSubmission'):
    class FormSubmission(AFormSubmission):
        pass


    __all__.append('FormSubmission')

from .snippets.person import APerson

if not is_model_registered('cms', 'Person'):
    @register_snippet
    class Person(TranslatableMixin, APerson):
        pass


    __all__.append('Person')

from .snippets.gallery import AGallery

if not is_model_registered('cms', 'Gallery'):
    @register_snippet
    class Gallery(AGallery):
        pass


    __all__.append('Gallery')

#  Pages


from .pages._generic import AGenericPage

if not is_model_registered('cms', 'GenericPage'):
    class GenericPage(AGenericPage):
        pass


    __all__.append('GenericPage')

from .pages.blog import ABlogIndexPage, ABlogPage, ABlogPageTag

if not is_model_registered('cms', 'BlogPageTag'):
    class BlogPageTag(ABlogPageTag):
        pass


    __all__.append('BlogPageTag')

if not is_model_registered('cms', 'BlogIndexPage'):
    class BlogIndexPage(ABlogIndexPage):
        pass


    __all__.append('BlogIndexPage')

if not is_model_registered('cms', 'BlogPage'):
    class BlogPage(ABlogPage):
        pass


    __all__.append('BlogPage')

from .pages.content import AContentPage

if not is_model_registered('cms', 'ContentPage'):
    class ContentPage(AContentPage):
        pass


    __all__.append('ContentPage')

from .pages.document import ADocumentPage

if not is_model_registered('cms', 'DocumentPage'):
    class DocumentPage(ADocumentPage):
        pass


    __all__.append('DocumentPage')

#  Settings

from .settings.webunity import AWebspaceSettings, AFounders

if not is_model_registered('cms', 'WebspaceSettings'):
    @register_setting
    class WebspaceSettings(AWebspaceSettings):
        pass


    __all__.append('WebspaceSettings')

if not is_model_registered('cms', 'Founders'):
    class Founders(AFounders):
        pass


    __all__.append('Founders')
