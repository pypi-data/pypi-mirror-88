from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
from django_celery_results.models import TaskResult
from wagtail.contrib.modeladmin.views import ModelFormView
from django.shortcuts import redirect

from webunity.bakery.tasks import build


class BuildView(ModelFormView):
    def get(self, request):
        build.delay()
        return redirect(self.get_success_url())


class TaskResultAdmin(ModelAdmin):
    model = TaskResult
    menu_label = 'Bakery'
    menu_icon = 'cog'
    menu_order = 2000
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('task_id', 'status', 'result', 'date_created')
    list_filter = ('status',)
    search_fields = ('task_name',)
    create_view_class = BuildView


modeladmin_register(TaskResultAdmin)
