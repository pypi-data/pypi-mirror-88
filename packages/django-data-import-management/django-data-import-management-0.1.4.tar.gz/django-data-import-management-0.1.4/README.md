# django-data-import-management

Django data import management application.


## Install

```
pip install django-data-import-management
```


## Usage

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_data_import_management',
    'example_app',
    ...
]
```

**example_app/import_workflow.py**

```
from django_data_import_management.models import DjangoDataImportWorkflow
from django_data_import_management.models import ParsedItem

class ExampleImportWorkflow(DjangoDataImportWorkflow):

    def do_parse(self):
        items = []
        for i in range(10):
            item = ParsedItem()
            info = str(i)
            data = {
                "index": 1,
            }
            item.mark_success(info, data)
            items.append(item)
        return items
    
    def do_import(self, import_items):
        for item in import_items:
            item.mark_success()
        return True

```

**example_app/apps.py**

```
class ExampleAppConfig(AppConfig):
    name = 'example_app'

    def ready(self):
        from django_data_import_management.models import register_django_data_import_workflow
        from .import_workflows import ExampleImportWorkflow
        register_django_data_import_workflow("Example Import", ExampleImportWorkflow)
```

**example_app/__init__.py**

```
default_app_config = "example_app.apps.ExampleAppConfig"
```

## Releases

### v0.1.4 2020/12/02

- First release.
