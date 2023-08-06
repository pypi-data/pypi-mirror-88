# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_lookups']

package_data = \
{'': ['*']}

install_requires = \
['Django>=1.11,<4']

setup_kwargs = {
    'name': 'django-lookups',
    'version': '0.1.2',
    'description': '',
    'long_description': '# django_lookups: Lookup Models for Django Applications\n\ndjango_lookups provides a LookupModel that many of us have written some variation 100\'s of times. Most of the applications we write have lookup tables (or should!) and we have boilerplate everywhere to manage constants. The aim of this library is to make working with lookup data in django easier.\n\nYou might have a constants repo / package / library that you share between your apps or services. Most of the time, instead of constants, those values really belong in lookup tables. Things like status int fields. If you have a django model with a field like `status = models.PositiveIntegerField` this library is probably for you!\n\n\nA trivial example showing how you might interact with an Order Status.\n```python\nclass OrderStatusTypes(django_lookups.LookupModel):\n    class Meta:\n        app_label = "my_app"\n        db_tabel = "my_table"\n\nclass Order(models.Model):\n    status = models.ForeignKey(OrderStatusTypes)\n    address = models.ForeignKey(...)\n    created = models.TimestampField()\n    changed = models.TimestampField()\n\n    @classmethod\n    def new_order(cls):\n        return cls.objects.create(\n            status=OrderStatusTypes.members.INITIATED.model,\n            ...\n        )\n```\n\n\nOnce you add this library as a dependency, and have created your first lookup model, you\'ll need to run a [data migration](https://docs.djangoproject.com/en/3.1/topics/migrations/#data-migrations) to add the lookup values to your table, or add data to your lookup tables manually. Once the data is there, your code can work with this data by name. No more need to keep constants libraries in sync when you add a new type/status etc!\n\n\nThis library is on pypi so you can run `pip install django_lookups` to get started or add it with the package manager of your choice.\n',
    'author': 'mistahchris',
    'author_email': 'chris@thesogu.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mistahchris/django_lookups',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
