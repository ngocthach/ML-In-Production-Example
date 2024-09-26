# Setup Django Project

## Install requirement
    pip install -r requirements.txt

## Start project
    django-admin startproject scraper

## Start sever
    python manage.py runserver

## Start app
    python manage.py startapp news

## Code tutorial
    
[Read here](Tutorial.md)

## Install Mysql Client
    Mac:
        brew install mysql-client pkg-config
        export PKG_CONFIG_PATH="$(brew --prefix)/opt/mysql-client/lib/pkgconfig"

    Ubuntu:
        sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config


## Deploy
    docker compose up -d --build
    docker compose down


## Get Telegram Group ID
    https://api.telegram.org/bot<api_token>/getUpdates


## References:
- Django Socket: https://blog.logrocket.com/django-channels-and-websockets/
- Django + React: https://medium.com/@martindegesus1/real-time-progress-bar-using-django-channels-react-and-websockets-7845342418d6
- Install MySql Client: https://github.com/PyMySQL/mysqlclient/blob/main/README.md#macos-homebrew
