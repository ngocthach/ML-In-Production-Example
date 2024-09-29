# Setup Django Project

## Install requirement
    pip install -r requirements.txt

## Start project
    django-admin startproject scraper

## Start sever
    python manage.py runserver

## Start app
    python manage.py startapp news

## Run server
    python manage.py collectstatic
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

## Install MariaDB
    cd mariadb
    create file .env from env
    docker compose up -d --build

## Code tutorial
    
[Read here](Tutorial.md)

## Deploy
    create file .env from env
    docker compose up -d --build
    docker compose down


## References:
- Install MySql Client: https://github.com/PyMySQL/mysqlclient/blob/main/README.md#macos-homebrew
