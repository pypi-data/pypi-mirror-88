from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.messages.api import success
from django.utils.translation import ngettext
from django.utils.translation import gettext as _

from .models import DjangoDataImportCase
from .models import DjangoDataImportItem
from .models import get_django_data_import_workflow_choices

def django_data_import_do_parse(modeladmin, request, queryset):
    for case in queryset.all():
        try:
            case.do_parse()
            modeladmin.message_user(request, _("Parse data file of case {case} success.").format(case=case.title), messages.SUCCESS)
        except Exception as error:
            modeladmin.message_user(request, _("Parse data file of case {case} failed: {message}").format(case=case.title, message=str(error)), messages.ERROR)
django_data_import_do_parse.short_description = _("Parse selected data files.")


def django_data_import_do_import(modeladmin, request, queryset):
    for case in queryset.all():
        try:
            case.do_import()
            modeladmin.message_user(request, _("Import data file of case {case} success.").format(case=case.title), messages.SUCCESS)
        except Exception as error:
            modeladmin.message_user(request, _("Import data file of case {case} failed: {message}").format(case=case.title, message=str(error)), messages.ERROR)
django_data_import_do_import.short_description = _("Import selected data files.")

def django_data_import_do_item_import(modeladmin, request, queryset):
    success_count = 0
    failed_count = 0
    for item in queryset.prefetch_related("case").all():
        try:
            success = item.do_import()
            if success:
                success_count += 1
            else:
                failed_count += 1
        except Exception as error:
            modeladmin.message_user(request, _("Import item {item} failed: {message}").format(item=item.pk, messages=str(error)), messages.ERROR)
            failed_count += 1

    if success_count:
        modeladmin.message_user(request, _("{success} items successfully imported.").format(success=success_count), messages.SUCCESS)
    if failed_count:
        modeladmin.message_user(request, _("{failed} items successfully imported.").format(failed=failed_count), messages.ERROR)
django_data_import_do_item_import.short_description = _("Import selected items.")

class DjangoDataImportCaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['import_workflow'] = forms.ChoiceField(
            choices=get_django_data_import_workflow_choices(),
            label=_("Import Workflow"),
        )

    class Meta:
        model = DjangoDataImportCase
        fields = "__all__"

class DjangoDataImportCaseAdmin(admin.ModelAdmin):
    form = DjangoDataImportCaseForm
    list_display = ["title", "import_workflow", "parse_result", "import_result"]
    list_filter = ["import_workflow"]
    actions = [
        django_data_import_do_parse,
        django_data_import_do_import,
    ]
    fieldsets = [
        (_("Import Settings"), {
            "fields": ["title", "import_workflow", "datafile"],
            "classes": ["django-data-import-case-admin-import-settings"],
        }),
        (_("Parse Resslt"), {
            "fields": ["parse_result", "parse_time", "parse_error"],
            "classes": ["django-data-import-case-admin-parse-result"],
        }),
        (_("Import Result"), {
            "fields": ["import_result", "import_time", "import_error"],
            "classes": ["django-data-import-case-admin-import-result"],
        })
    ]
    readonly_fields = ["parse_result", "parse_time", "parse_error", "import_result", "import_time", "import_error"]


class DjangoDataImportItemAdmin(admin.ModelAdmin):
    list_display = ["id", "success", "info", "import_success", "case"]
    list_filter = ["case", "success", "import_success"]
    search_fields = ["info", "json_data"]
    actions = [
        django_data_import_do_item_import,
    ]
    readonly_fields = ["case", "success", "info", "add_time", "json_data", "import_success", "import_time", "import_error"]
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("case")

admin.site.register(DjangoDataImportCase, DjangoDataImportCaseAdmin)
admin.site.register(DjangoDataImportItem, DjangoDataImportItemAdmin)
