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
    CELERY_RESULT_BACKEND = "django-db"
    
    # Define the content types for serialization
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    
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


## Config Celery
    
    import os
    from celery import Celery
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraper.settings")
    app = Celery("scraper")
    
    app.config_from_object("django.conf:settings", namespace="CELERY")
    
    # Load task modules from all registered Django app configs.
    app.autodiscover_tasks()
    
    app.conf.update(result_extended=True,)


## Edit __init__.py
    from .celery import app as celery_app
    import pymysql
    
    pymysql.install_as_MySQLdb()
    
    __all__ = ("celery_app",)


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

    def create_logger(name, level=logging.DEBUG):
        logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(logging.StreamHandler())
        return logger


## Add tasks.py
    import logging

    from celery import shared_task
    from .utils import crawl_website, extract_title
    
    logger = logging.getLogger(__name__)
    
    @shared_task
    def crawl_news_task(url):
        html = crawl_website(url)
        title = extract_title(html)
        logger.info(f"Collected {title}")
    return {"title": title}


## Add news/__init__.py
    default_app_config = 'new.apps.NewsConfig'


## Add news/views.py

    import time

    from celery.result import AsyncResult
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    from django.views.decorators.http import require_POST
    
    from .tasks import crawl_news_task
    from .utils import extract_post_request, create_logger
    
    logger = create_logger(__name__)
    
    @require_POST
    @csrf_exempt
    def crawl_news(request):
        json_data = extract_post_request(request)
        url = json_data.get("url")
    
        task = crawl_news_task.delay(url)
        return JsonResponse({"task_id": task.id}, status=200)


    @csrf_exempt
    def get_crawl_result(request, task_id):
        start_time = time.time()
        while True:
            task_result = AsyncResult(task_id)
            task_status = task_result.status
            logger.info(f"Task result: {task_result.result}")
    
            if task_status == 'PENDING':
                if time.time() - start_time > 60:  # 60 seconds timeout
                    return {
                        "task_id": task_id,
                        "task_status": task_result.status,
                        "task_result": task_result.result,
                        "error_message": "Service timeout, retry please"
                    }
                else:
                    time.sleep(0.5)  # sleep for 0.5 seconds before retrying
            else:
                result = {
                    "task_id": task_id,
                    "task_status": task_result.status,
                    "task_result": task_result.result
                }
                return JsonResponse(result, status=200)


## Update utils.py call ML model
    def detect_sentiment(text):
        payload = json.dumps({ "text": text})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", ml_host, headers=headers, data=payload)
        return response.text

## Update tasks.py call ML model
    @shared_task
    def crawl_news_task(url):
        html = crawl_website(url)
        title = extract_title(html)
        logger.info(f"Collected {title}")
    
        sentiment = detect_sentiment(title)
        logger.info(f"Detect {sentiment}")
    
        return {"title": title, "sentiment": sentiment}


## Run server
    cd backend
    docker compose up -d --build

