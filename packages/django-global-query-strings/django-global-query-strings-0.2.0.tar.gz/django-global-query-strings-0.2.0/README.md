# Django global query strings
[![Python 3](https://img.shields.io/badge/python-3.6|3.7|3.8-blue.svg)](https://www.python.org/downloads/release/python-270/) 
[![Django 2](https://img.shields.io/badge/django-2.x-blue.svg)](https://docs.djangoproject.com/en/2.2/)
![Python CI](https://github.com/briefmnews/django-global-query-strings/workflows/Python%20CI/badge.svg)
[![codecov](https://codecov.io/gh/briefmnews/django-global-query-strings/branch/main/graph/badge.svg?token=vf2gtEaMBp)](https://codecov.io/gh/briefmnews/django-global-query-strings)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

`Django global query strings` allows adding query strings (query params) globally.  
The app looks for all the `<a>` tags in a html content thanks to [BeautifulSoup](https://pypi.org/project/beautifulsoup4/#description).

There are two ways of using the app. Each way can be used separately or conjointly:
* Using the middleware `GlobalQueryStringsMiddleware`
* Using the utility function `add_query_strings_to_links`

## Installation
Install with pip:
```
pip install django-global-query-strings
```

## Setup
In order to make `django-global-query-strings` works, you'll need to follow the steps below:

### Settings
First, you need to add the app and the middleware to your settings. The middleware is optional depending on your usage:
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',

    'global_query_strings',
    ...
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    'global_query_strings.middleware.GlobalQueryStringsMiddleware',
    ...
)
```

### Settings
Here is the list of all the settings with their default values:
```python
GLOBAL_QUERY_STRINGS_IGNORE_URLS = []
GLOBAL_QUERY_STRINGS_IGNORE_RELATIVE_PATHS = False
GLOBAL_QUERY_STRINGS_PARAMS = {}
```

#### GLOBAL_QUERY_STRINGS_IGNORE_URLS 
`GLOBAL_QUERY_STRINGS_IGNORE_URLS` takes a list of domain name or urls e.g.: `["example.com", "https://www.foo.org"]`. When the html parser finds those values, the global query strings won't be added to the urls.

#### GLOBAL_QUERY_STRINGS_IGNORE_RELATIVE_PATHS 
`GLOBAL_QUERY_STRINGS_IGNORE_RELATIVE_PATHS` is a boolean. When set to `True`, the parser will ignore relative paths.

#### GLOBAL_QUERY_STRINGS_PARAMS 
`GLOBAL_QUERY_STRINGS_PARAMS` takes a dictionary of global query strings to set e.g.: `{"foo": "bar", "lorem": "ipsum"}`. The query strings found in `GLOBAL_QUERY_STRINGS_PARAMS` would be replaced / added to the urls found by the parser.

## Usage
Here is an example of input / output with the following settings:
```python
GLOBAL_QUERY_STRINGS_IGNORE_URLS = ["example.com", "https://www.foo.org"]
GLOBAL_QUERY_STRINGS_IGNORE_RELATIVE_PATHS = True
GLOBAL_QUERY_STRINGS_PARAMS = {"foo": "bar", "lorem": "ipsum"}
```

__Input__:
```html
<html lang="en">
    <body>
        <a href="https://www.foo.org">Lorem Ipsum</a> is simply dummy text of the printing and typesetting industry.
        <a href="https://foo.org">Lorem Ipsum</a> has been the industry's standard dummy text ever since the 1500s,
        when an unknown printer took a galley of type and scrambled it to make a type specimen book.
        It has survived not only <a href="https://www.bar.com">five centuries</a>, but also the leap into electronic
        typesetting, <a href="/lorem/ipsum">remaining essentially</a> unchanged.
        It was popularised in the 1960s with the release of <a href="https://www.bar.com?example=true">Letraset sheets</a>
        containing Lorem Ipsum passages, and more recently with desktop <a href="https://www.foo.org?foo=ipsum">publishing software</a>
        like Aldus PageMaker including versions of Lorem Ipsum.
    </body>
</html>
```

__Output__:
```html
<html lang="en">
    <body>
        <a href="https://www.foo.org">Lorem Ipsum</a> is simply dummy text of the printing and typesetting industry.
        <a href="https://foo.org?foo=bar&lorem=ipsum">Lorem Ipsum</a> has been the industry's standard dummy text ever since the 1500s,
        when an unknown printer took a galley of type and scrambled it to make a type specimen book.
        It has survived not only <a href="https://www.bar.com?foo=bar&lorem=ipsum">five centuries</a>, but also the leap into electronic
        typesetting, <a href="/lorem/ipsum">remaining essentially</a> unchanged.
        It was popularised in the 1960s with the release of <a href="https://www.bar.com?example=true&foo=bar&lorem=ipsum">Letraset sheets</a>
        containing Lorem Ipsum passages, and more recently with desktop <a href="https://www.foo.org?foo=bar&lorem=ipsum">publishing software</a>
        like Aldus PageMaker including versions of Lorem Ipsum.
    </body>
</html>

```

## Tests
Testing is managed by `pytest`. Required package for testing can be installed with:
```
pip install -r test_requirements.txt
```

To run testing locally:
```
pytest
```
