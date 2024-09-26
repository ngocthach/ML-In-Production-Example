## Code Tutorial

## Django Setting
    # Load config
    from decouple import config

    # Allow host
    ALLOWED_HOSTS = ['*']

    # Add App
    INSTALLED_APPS = [
        'news',
        'rest_framework',
        'rest_framework.authtoken',
        'django_celery_beat',
        'django_celery_results',
    ]

    # Database
    db_password = os.environ.get("MYSQL_ROOT_PASSWORD", "")
    db_host = os.environ.get("MYSQL_HOST", "0.0.0.0")
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'scrape',
            'USER': 'root',
            'PASSWORD': db_password,
            'HOST': db_host,
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_unicode_ci',
            }
        }
    }

    # Celery settings

    # Broker_connection_retry_on_startup
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    
    # This configures Redis as the datastore between Django + Celery
    CELERY_BROKER_URL = config("CELERY_BROKER_REDIS_URL", default="redis://0.0.0.0:6379")
    
    # Allows you to schedule items in the Django admin.
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

    # Django Rest Framework

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 100,
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ],
    }

    # Static file
    STATIC_URL = '/statics/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'statics')
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


## Config Celery
    
    import os
    from celery import Celery
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraper.settings")
    app = Celery("scraper")
    
    app.config_from_object("django.conf:settings", namespace="CELERY")
    
    # Load task modules from all registered Django app configs.
    app.autodiscover_tasks()
    
    app.conf.update(result_extended=True,)


## Add url to scraper/urls.py
    Edit urls.py
    path("news/", include("news.urls")),

## Add news/urls.py
    from django.urls import path
    from . import views
    
    app_name = "news"
    
    urlpatterns = [
        path("crawl", views.crawl_news, name="crawl_news"),
        path("crawl/<str:task_id>", views.get_crawl_result, name="get_crawl_result"),
    ]

## Add news/utils.py
    import json
    import logging
    import requests
    from bs4 import BeautifulSoup
    
    
    def extract_post_request(request):
        try:
            return json.loads(request.body.decode('utf-8'))
        except ValueError as err:
            logging.error(err)
            return {}
    
    
    def crawl_website(url):
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
        return response.content
    
    
    def extract_title(html):
        soup = BeautifulSoup(html, "html.parser")
    
        try:
            title = soup.find('h1', class_='title-detail').text.strip()
        except AttributeError:
            title = 'N/A'

    return title


## Add tasks.py
    import logging

    from celery import shared_task
    from .utils import crawl_website, extract_title
    
    logger = logging.getLogger(__name__)
    
    @shared_task
    def crawl_news_task(url):
        html = crawl_website(url)
        title = extract_title(html)
    return {"title": title}
