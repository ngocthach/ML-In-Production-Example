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
    python manage.py makemigrations
    
    python manage.py runserver

## Install MariaDB
    cd mariadb
    docker compose up -d --build

## Code tutorial
    
[Read here](Tutorial.md)

## Deploy
    docker compose up -d --build
    docker compose down


## References:
- Install MySql Client: https://github.com/PyMySQL/mysqlclient/blob/main/README.md#macos-homebrew
