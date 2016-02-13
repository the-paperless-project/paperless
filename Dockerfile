FROM ubuntu:14.04

RUN mkdir -p /opt/paperless/scripts
WORKDIR /opt/paperless

COPY scripts/vagrant-provision /opt/paperless/scripts/
COPY requirements.txt /opt/paperless/

RUN bash /opt/paperless/scripts/vagrant-provision

ADD . /opt/paperless/

WORKDIR /opt/paperless/src/

ENV PYTHONPATH /usr/local/lib/python3.4/dist-packages/:/usr/local/lib/python2.7/dist-packages/:/usr/lib/python3/dist-packages/
ENV PAPERLESS_PASSPHRASE some-secret-string

RUN python manage.py migrate

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
