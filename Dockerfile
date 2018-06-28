FROM alpine:edge


RUN apk update && apk upgrade \
    && apk add --update \
    python3 \
    python3-dev \
    py-pip \
    build-base \
  && pip install virtualenv

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app


ADD crontab.txt /crontab.txt
ADD entry.sh /entry.sh


CMD ["/entry.sh"]