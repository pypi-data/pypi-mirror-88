import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'asdf1234')
# INDEX_NAME = os.environ.get('INDEX_NAME', 'idx')

SERVER_NAME = os.environ.get('DOCS_SERVER_NAME')

LOGLEVEL = os.environ.get('LOGLEVEL', 10)

VERSION = os.environ.get('VERSION')
SOURCE = os.environ.get('SOURCE')
"""GitHub repo containing the documentation source."""
BUILD_TIME = os.environ.get('BUILD_TIME')

STATIC_ROOT = os.environ.get('STATIC_ROOT', 'static')
TEMPLATE_ROOT = os.environ.get('TEMPLATE_ROOT', 'templates')

EXTERNAL_URL_SCHEME = os.environ.get('EXTERNAL_URL_SCHEME', 'https')
BASE_SERVER = os.environ.get('BASE_SERVER', 'arxiv.org')
URLS = [
    ("home", "/", BASE_SERVER),
    ("archive", "/archive/<archive>", BASE_SERVER),
    ("search_box", "/search", BASE_SERVER),
    ("clickthrough", "/ct", BASE_SERVER),
    ("search_archive", "/search/<archive>", BASE_SERVER),
    ("search_advanced", "/search/advanced", BASE_SERVER),
]


"""
Flask-S3 plugin settings.

See `<https://flask-s3.readthedocs.io/en/latest/>`_.
"""
FLASKS3_BUCKET_NAME = os.environ.get('FLASKS3_BUCKET_NAME', 'some_bucket')
FLASKS3_CDN_DOMAIN = os.environ.get('FLASKS3_CDN_DOMAIN', 'static.arxiv.org')
FLASKS3_USE_HTTPS = os.environ.get('FLASKS3_USE_HTTPS', 1)
FLASKS3_FORCE_MIMETYPE = os.environ.get('FLASKS3_FORCE_MIMETYPE', 1)
FLASKS3_ACTIVE = bool(int(os.environ.get('FLASKS3_ACTIVE', 0)))

# AWS credentials.
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'nope')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'nope')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

SOURCE_PATH = os.environ.get('SOURCE_PATH')
BUILD_PATH = os.environ.get('BUILD_PATH')
SITE_NAME = os.environ.get('SITE_NAME', 'arxiv')
SITE_URL_PREFIX = os.environ.get('SITE_URL_PREFIX', '/')
SITE_HUMAN_SHORT_NAME = os.environ.get('SITE_HUMAN_SHORT_NAME', 'Static')
SITE_HUMAN_NAME = os.environ.get('SITE_HUMAN_NAME', 'arXiv Static Pages')
SITE_SEARCH_ENABLED = bool(int(os.environ.get('SITE_SEARCH_ENABLED', 1)))
APP_VERSION = "0.1"

JIRA_FEEDBACK_ENABLED = bool(int(os.environ.get("JIRA_FEEDBACK_ENABLED", "0")))
JIRA_VERSION = os.environ.get("JIRA_VERSION", "14219")      # docs-0.2
JIRA_COMPONENT = os.environ.get("JIRA_COMPONENT", "12154")    # Help pages
JIRA_COLLECTOR_URL = os.environ.get(
    "JIRA_COLLECTOR_URL",
    "https://arxiv-org.atlassian.net/s/d41d8cd98f00b204e9800998ecf8427e-T/-2rfjj7/b/29/a44af77267a987a660377e5c46e0fb64/_/download/batch/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector.js?locale=en-US&collectorId=9f4c36dd"
)
RELEASE_NOTES_URL = "https://"
RELEASE_NOTES_TEXT = "v0.2 released 2019-02-11"

RELATIVE_STATIC_PATHS = bool(int(os.environ.get('RELATIVE_STATIC_PATHS', '0')))
"""If true, all static paths are under ``SITE_URL_PREFIX``."""

DOCS_ANALYTICS_ENABLED = bool(int(os.environ.get("BROWSE_ANALYTICS_ENABLED", "1")))
"""Enable/disable web analytics."""
