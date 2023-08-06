import logging
from django.db import models
from django.conf import settings
from django.template.response import TemplateResponse
from django.http import HttpResponse

logger = logging.getLogger('bakery')


class BuildableModel(models.Model):
    detail_views = []

    def _get_view(self, name):
        from django.urls import get_callable
        return get_callable(name)

    def _build_related(self):
        pass

    def _build_extra(self):
        pass

    def _unbuild_extra(self):
        pass

    def build(self):
        for detail_view in self.detail_views:
            view = self._get_view(detail_view)
            view().build_object(self)
        self._build_extra()
        self._build_related()

    def unbuild(self):
        for detail_view in self.detail_views:
            view = self._get_view(detail_view)
            view().unbuild_object(self)
        self._unbuild_extra()
        # _build_related again to kill the object from RSS etc.
        self._build_related()

    def get_absolute_url(self):
        return self.get_full_url()

    class Meta:
        abstract = True


class BakeryMixin(BuildableModel):
    detail_views = ['webunity.bakery.views.wagtail.AllBuildablePagesView']

    def serve(self, request, extra_path_file='', *args, **kwargs):
        is_building = request.GET.get('build', False)
        request.is_preview = getattr(request, 'is_preview', False)

        #  Remove settings.DEBUG if you want to test static page

        if settings.DEBUG or request.is_preview or is_building:
            logger.debug('Serving TemplateResponse')
            return TemplateResponse(
                request,
                self.get_template(request),
                self.get_context(request, *args, **kwargs)
            )
        else:
            site = self.get_site()
            path_file = self.relative_url(site)
            index = 'index.html' if request.user_agent.is_pc else 'index-mobile.html'
            with open(settings.BUILD_DIR + '/' + site.hostname + '/' + path_file + extra_path_file + index, "rb") as fd:
                compressed = fd.read()
                response = HttpResponse(compressed)
                response['Content-Encoding'] = 'gzip'
                response['Content-Length'] = str(len(compressed))
                logger.debug('Serving Static File')
                return response

    class Meta:
        abstract = True
