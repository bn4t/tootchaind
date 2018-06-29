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


COPY . /app
RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt

ADD crontab.txt /crontab.txt
ADD entry.sh /entry.sh

RUN chmod 755 /entry.sh
RUN /usr/bin/crontab /crontab.txt

CMD ["/entry.sh"]