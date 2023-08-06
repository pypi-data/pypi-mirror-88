# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtailsnippetscopy']

package_data = \
{'': ['*'], 'wagtailsnippetscopy': ['templates/wagtailsnippetscopy/*']}

install_requires = \
['django>=2.2,<3.2', 'wagtail>=2.11']

setup_kwargs = {
    'name': 'wagtailsnippetscopy',
    'version': '0.3.0',
    'description': 'Copy A Snippet Feature for Wagtail CMS',
    'long_description': '# \'Copy A Snippet\' Feature for Wagtail CMS\n\nYou can now "copy" snippets (non-page models) in Wagtail CMS\n\n## Installation\n\n1. Install the python package wagtailsnippetscopy from pip\n\n`pip install wagtailsnippetscopy`\n\nAlternatively, you can install download or clone this repo and call `pip install -e .`.\n\n2. Add to INSTALLED_APPS in your **settings.py**:\n\n`\'wagtailsnippetscopy\',`\n\n3. Register a model (with a title field name) you wish to enable copy functionality for:\n\n```python\nfrom wagtailsnippetscopy.registry import snippet_copy_registry\n\nsnippet_copy_registry.register(YourModel, {})\n```\n\n4. Add SnippetCopyMixin to your Snippet model in order to enable get_copy_url callback() for the model:\n\n```python\nfrom wagtailsnippetscopy.models import SnippetCopyMixin\n\nclass Graph(SnippetCopyMixin, models.Model):\n```\n\n5. If you wish copy link to automatically appear in modeladmin list you should add SnippetCopyModelAdminMixin to the ModelAdmin class:\n\nIn admin.py:\n\n```python\nfrom wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register\nfrom wagtailsnippetscopy.admin import SnippetCopyModelAdminMixin\nfrom .models import YourModel\n\nclass YourModelAdmin(SnippetCopyModelAdminMixin, ModelAdmin):\n    model = YourModel\n\nmodeladmin_register(GraphAdmin)\n```\n\n6. Copy link follows the following pattern:\n\n```\n/admin/copy-snippet/<app_label>/<model_name>/<object_id>/\n```\n\n## Bugs and suggestions\n\nIf you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.\n\n[https://github.com/timonweb/wagtailsnippetscopy/issues](https://github.com/timonweb/wagtailsnippetscopy/issues)\n\nby [Tim Kamanin](https://timonweb.com/wagtail-developer/)\n',
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://timonweb.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
