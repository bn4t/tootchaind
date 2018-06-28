FROM alpine:edge


RUN apk update && apk upgrade \
    && apk add python3

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app


ADD crontab.txt /crontab.txt
ADD entry.sh /entry.sh


CMD ["/entry.sh"]