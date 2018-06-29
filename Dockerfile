FROM alpine:edge


RUN apk update && apk upgrade \
    && apk add --update \
    python3 \
    python-dev \
    libffi \
    libffi-dev \
    py3-cffi \
    py2-cffi \
    openssl-dev \
    libssl1.0 \
    python3-dev \
    py-pip \
    build-base \
    bash \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*


COPY . /app/

RUN virtualenv -p python3 /env && /env/bin/pip3 install -r /app/requirements.txt

COPY crontab.txt /crontab.txt
COPY entry.sh /entry.sh

RUN chmod 755 /entry.sh
RUN /usr/bin/crontab /crontab.txt

CMD ["/entry.sh"]