#!/usr/bin/env python
"""

source: https://github.com/carljm/django-model-utils/blob/f8a7c50/runtests.py

"""
import os
import sys

from django.conf import settings
import django


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

LOGGING_CONFIG = {
    'version': 1,
    # 'disable_existing_loggers': True,
    'disable_existing_loggers': False,
    'formatters': {
        'custom': {
            # available LogRecord attributes:
            # http://docs.python.org/library/logging.html#logrecord-attributes
            'format': ('%(levelname)s [%(asctime)s] %(name)s | '
                       '%(funcName)s:%(lineno)d | %(message)s\n')
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'custom'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', ],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', ],
            'level': 'WARNING',
            'propagate': False,
        },
        'lu_dj_utils': {
            'handlers': ['console', ],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}

DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=(
        'django.contrib.sites',  # used by `lu_dj_utils.urls`
        'lu_dj_utils',
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            }
        },
    TEMPLATE_DIRS=(
        os.path.join(ROOT_DIR, 'tests', 'templates'),
    ),
    LOGGING=LOGGING_CONFIG,
    SILENCED_SYSTEM_CHECKS=[
        '1_7.W001',  # MIDDLEWARE_CLASSES is not set
    ],
)


def runtests():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    # Compatibility with Django 1.7's stricter initialization
    if hasattr(django, 'setup'):
        django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        from django.test.runner import DiscoverRunner
        runner_class = DiscoverRunner
        test_args = ['tests']
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner
        runner_class = DjangoTestSuiteRunner
        test_args = ['tests']

    failures = runner_class(
        verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
