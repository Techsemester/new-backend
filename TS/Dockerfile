FROM python:3.8-alpine

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN apk update \
    && apk add --update --no-cache --virtual build-deps gcc python3 musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add --no-cache file-dev \
    && pip install filemagic \
    && apk add libc-dev linux-headers libffi-dev openssl-dev cargo \
#    && apk add libc-dev linux-headers libressl-dev  libffi-dev openssl-dev cargo \
    && apk add jpeg-dev zlib-dev libjpeg \
    && python3 -m pip install --upgrade cryptography \
    && pip install Pillow \
    && apk del build-deps

RUN pip install -r /requirements.txt

RUN mkdir /usr/src/bic

COPY ./ /usr/src/bic

WORKDIR /usr/src/bic

COPY ./techsemester /


COPY ./entrypoint.sh /

RUN mkdir -p /var/www/cerbot
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/media_url

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]
