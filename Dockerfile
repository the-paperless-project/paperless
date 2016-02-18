FROM ubuntu:14.04

RUN mkdir -p /opt/paperless/scripts
WORKDIR /opt/paperless

RUN apt-get install -y tofrodos

COPY scripts/vagrant-provision /opt/paperless/scripts/
COPY requirements.txt /opt/paperless/

RUN fromdos /opt/paperless/scripts/vagrant-provision
RUN bash /opt/paperless/scripts/vagrant-provision

ADD . /opt/paperless/

WORKDIR /opt/paperless/src/

ENV PYTHONPATH /usr/local/lib/python3.4/dist-packages/:/usr/local/lib/python2.7/dist-packages/:/usr/lib/python3/dist-packages/
ENV PAPERLESS_PASSPHRASE some-secret-string
ENV CONSUMPTION_DIR /opt/consumption

ENV USERNAME admin
ENV EMAIL admin@example.com
ENV PASSWORD paperless

RUN python manage.py migrate

EXPOSE 8000

CMD echo "from django.contrib.auth.models import User; import os; User.objects.create_superuser(os.environ.get('USERNAME'), os.environ.get('EMAIL'), os.environ.get('PASSWORD'))" | python manage.py shell && python manage.py runserver 0.0.0.0:8000
