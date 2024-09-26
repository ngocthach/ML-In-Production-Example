## Create network
    docker network create internal_tool

## Run docker
    docker compose up -d

## Stop docker
    docker compose down

## Install Mysql-client (for test)
    Ubuntu:
        sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

    MacOs:
        brew install mysql-client pkg-config
        export PKG_CONFIG_PATH="$(brew --prefix)/opt/mysql-client/lib/pkgconfig"

    export MYSQLCLIENT_LDFLAGS=$(pkg-config --libs mysqlclient)
    export MYSQLCLIENT_CFLAGS=$(pkg-config --cflags mysqlclient)
    pip install mysqlclient

## Access
    docker exec -it mariadb-db bash
    mysql -u root -p

    CREATE DATABASE scraper CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
