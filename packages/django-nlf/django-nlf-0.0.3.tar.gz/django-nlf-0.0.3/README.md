[![PyPi Version](https://img.shields.io/pypi/v/django-nlf)](https://pypi.org/project/django-nlf/)
[![PyPi Downloads](https://img.shields.io/pypi/dw/django-nlf)](https://pypi.org/project/django-nlf/)
![Tests](https://github.com/hodossy/django-nlf/workflows/Unit%20tests/badge.svg?branch=main)
![Weekly](https://github.com/hodossy/django-nlf/workflows/Weekly/badge.svg?branch=main)
[![Documentation](https://img.shields.io/readthedocs/django-nlf)](https://django-nlf.readthedocs.io/en/latest/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# django-nlf

Django Natural Language Filter

## Installation

Install using `pip`,

```
pip install django-nlf
```

Then you can use the `DjangoNLFilter` with a queryset and a string, containing the filter expression. Please see the [Language Reference]() for more details.

```python
from django_nlf import DjangoNLFilter
from .models import Article

nl_filter = DjangoNLFilter()
qs = Article.objects.all()
q = 'author.username is john or title contains news'
# equivalent to Article.objects.filter(Q(author__username="user") | Q(title__icontains="news"))
articles = nl_filter.filter(qs, q)

# Nested logical operators are also supported:
q = 'author.username is john and (title contains news or created_at <= 2020-06-05)'
# equivalent to
# Article.objects.filter(
#   Q(author__username="user") & (Q(title__icontains="news") | Q(created_at__lte="2020-06-05"))
# )
articles = nl_filter.filter(qs, q)
```

## Rest framework integration

You just need to simply add the natural language filter backend to your filter backends list.

```
REST_FRAMEWORK = {
  ...
  'DEFAULT_FILTER_BACKENDS': (
    'django_nlf.rest_framework.DjangoNLFilterBackend',
  ),
  ...
}
```
