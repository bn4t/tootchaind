FROM alpine:edge


RUN apk update && apk upgrade \
    && apk add --update \
    python3 \
    python3-dev \
    py-pip \
    build-base \
    bash \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

WORKDIR /app

ONBUILD COPY . /app
ONBUILD RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt

COPY . /usr/src/app


ADD crontab.txt /crontab.txt
ADD entry.sh /entry.sh

RUN chmod 755 /entry.sh
RUN /usr/bin/crontab /crontab.txt

CMD ["/entry.sh"]