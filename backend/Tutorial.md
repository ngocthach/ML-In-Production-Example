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
            'NAME': 'scraper',
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

