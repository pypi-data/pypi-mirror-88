
import json

from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext as _
from django_safe_fields.fields import SafeCharField
from django_safe_fields.fields import SafeTextField

from .settings import DJANGO_DATA_IMPORT_MANAGEMENT_DATA_FILE_UPLOAD_TO
from .settings import SAFE_FIELD_PASSWORDS

DJANGO_DATA_IMPORT_WORKFLOWS = {
}

class ParsedItem(object):
    def __init__(self, success=None, info=None, data=None):
        self.success = success
        self.info = info
        self.data = data
    
    def mark_success(self, info, data):
        self.success = True
        self.info = info
        self.data = data
    
    def mark_failed(self, error_message, error_data=None):
        self.success = False
        self.info = error_message
        self.data = error_data


class DjangoDataImportWorkflow(object):

    def __init__(self, datafile):
        self.datafile = datafile

    def do_parse(self):
        raise NotImplementedError()

    def do_import(self, imported_items):
        raise NotImplementedError()

def register_django_data_import_workflow(name, workflow):
    DJANGO_DATA_IMPORT_WORKFLOWS[name] = workflow


def get_django_data_import_workflow_choices():
    choices = [
        (None, "-"*40),
    ]
    for name in DJANGO_DATA_IMPORT_WORKFLOWS:
        choices.append((name, name))
    return choices

class DjangoDataImportCase(models.Model):
    SUCCESS = 10
    FAILED = 20
    PARTLY_FAILED = 30

    RESULT_CHOICES = [
        (SUCCESS, _("Success")),
        (FAILED, _("Failed")),
        (PARTLY_FAILED, _("Partly Failed")),
    ]

    title = SafeCharField(max_length=512, verbose_name=_("Title"), password=SAFE_FIELD_PASSWORDS["django_data_import_management.DjangoDataImportCase.title"])
    import_workflow = SafeCharField(max_length=512, verbose_name=_("Import Workflow"), password=SAFE_FIELD_PASSWORDS["django_data_import_management.DjangoDataImportCase.import_workflow"])
    datafile = models.FileField(upload_to=DJANGO_DATA_IMPORT_MANAGEMENT_DATA_FILE_UPLOAD_TO, verbose_name=_("Data File"))
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    mod_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"))

    parse_result = models.IntegerField(choices=RESULT_CHOICES, null=True, blank=True, verbose_name=_("Parse Result"))
    parse_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Parse Time"))
    parse_error = SafeTextField(null=True, blank=True, verbose_name=_("Parse Error"), password=SAFE_FIELD_PASSWORDS["django_data_import_management.DjangoDataImportCase.parse_error"])

    import_result = models.IntegerField(choices=RESULT_CHOICES, null=True, blank=True, verbose_name=_("Import Result"))
    import_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Import Time"))
    import_error = SafeTextField(null=True, blank=True, verbose_name=_("Import Error"), password=SAFE_FIELD_PASSWORDS["django_data_import_management.DjangoDataImportCase.import_error"])

    class Meta:
        ordering = ["-pk"]
        verbose_name = _("Django Data Import Case")
        verbose_name_plural = _("Django Data Import Cases")

    def __str__(self):
        return self.title

    def get_workflow_class(self):
        return DJANGO_DATA_IMPORT_WORKFLOWS.get(self.import_workflow, None)

    def get_workflow(self):
        workflow_class = self.get_workflow_class()
        if not workflow_class:
            raise RuntimeError(_("Unknown import workflow!"))
        workflow = workflow_class(self.datafile.path)
        return workflow

    def do_parse(self):
        try:
            workflow = self.get_workflow()
            rows = workflow.do_parse()
            DjangoDataImportItem.objects.filter(case=self).delete()
            items = []
            success_count = 0
            failed_count = 0
            for row in rows:
                item = DjangoDataImportItem()
                item.case = self
                item.success = row.success
                item.info = row.info
                item.data = row.data
                items.append(item)
                if row.success:
                    success_count += 1
                else:
                    failed_count += 1
            DjangoDataImportItem.objects.bulk_create(items, batch_size=200)
            if success_count and failed_count:
                self.parse_result = self.PARTLY_FAILED
            elif failed_count:
                self.parse_result = self.FAILED
            else:
                self.parse_result = self.SUCCESS
            self.parse_time = timezone.now()
            self.parse_error = None
            self.save()
        except Exception as error:
            self.parse_result = self.FAILED
            self.parse_time = timezone.now()
            self.parse_error = str(error)
            self.save()
        return True

    def do_import(self, items=None):
        try:
            workflow = self.get_workflow()
            import_items = items or list(self.items.filter(success=True).all())
            workflow.do_import(import_items)
            DjangoDataImportItem.objects.bulk_update(import_items, ["import_success", "import_error", "import_time"], batch_size=200)
            success_count = 0
            failed_count = 0
            for item in import_items:
                if item.import_success:
                    success_count += 1
                else:
                    failed_count += 1
            if success_count and failed_count:
                self.import_result = self.PARTLY_FAILED
            elif failed_count:
                self.import_result = self.FAILED
            else:
                self.import_result = self.SUCCESS
            self.import_time = timezone.now()
            self.import_error = None
            self.save()
        except Exception as error:
            self.import_result = self.FAILED
            self.import_time = timezone.now()
            self.import_error = str(error)
            self.save()
        return True

class DjangoDataImportItem(models.Model):
    case = models.ForeignKey(DjangoDataImportCase, on_delete=models.CASCADE, related_name="items", verbose_name=_("Django Data Import Case"))

    success = models.NullBooleanField(verbose_name=_("Parse Success"))
    info = SafeCharField(max_length=512, null=True, blank=True, verbose_name=_("Item Information"), password=SAFE_FIELD_PASSWORDS["django_data_import_management.DjangoDataImportItem.info"])
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Parsed Time"))
    json_data = SafeTextField(null=True, blank=True, verbose_name=_("Data"), password=SAFE_FIELD_PASSWORDS["django_data_import_management.DjangoDataImportItem.json_data"])

    import_success = models.NullBooleanField(default=None, verbose_name=_("Import Success"))
    import_error = SafeTextField(null=True, blank=True, verbose_name=_("Import Error Message"), password=SAFE_FIELD_PASSWORDS["django_data_import_management.DjangoDataImportItem.import_error"])
    import_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Import Time"))

    class Meta:
        verbose_name = _("Django Data Import Item")
        verbose_name_plural = _("Django Data Import Items")

    def get_json_data(self):
        if not self.json_data:
            return None
        else:
            return json.loads(self.json_data)
    
    def set_json_data(self, value):
        self.json_data = json.dumps(value)
    
    data = property(get_json_data, set_json_data)


    def mark_success(self):
        self.import_success = True
        self.import_time = timezone.now()
        self.import_error = None
    
    def mark_failed(self, error):
        self.import_success = False
        self.import_time = timezone.now()
        self.import_error = str(error)

    def do_import(self):
        self.case.do_import([self])
        return self.import_success