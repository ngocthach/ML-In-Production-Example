FROM python:3.10.14-slim-bullseye

RUN apt update -y \
    && apt-get install \
        python3-dev \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config -y \
    && apt-get clean

# set work directory
WORKDIR /usr/src/app/scraper

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=$PYTHONPATH:/usr/src/app/

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/scraper/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
