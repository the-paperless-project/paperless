FROM ubuntu:20.04 as builder

ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential autoconf automake libtool \
  python3 \
  python3-venv \
  python3-setuptools \
  python3-wheel \
  pipenv \
  python3-pip

# Get build deps
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  libpython3.8-dev \
  libpq-dev \
  libmariadb-dev \
  libpoppler-cpp-dev \
  libxslt-dev \
  libxml2-dev

# get dependencies
WORKDIR /usr/src/paperless
COPY Pipfile* .
RUN pipenv lock --keep-outdated --requirements > requirements.txt

ENV VIRTUAL_ENV=/usr/src/paperless
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install -r requirements.txt

FROM jbarlow83/ocrmypdf

ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
  python3.8 \
  python3-venv \
  gnupg \
  imagemagick \
  optipng \
  libpoppler-cpp0v5 \
  sudo \
  gettext \
  mariadb-client \
  libmariadb3 \
  libmagic1 \
  curl && \
  rm -rf /var/lib/apt/lists/*

# Set export and consumption directories
ENV PAPERLESS_EXPORT_DIR=/export
ENV PAPERLESS_CONSUMPTION_DIR=/consume

# Create the directories and user
RUN mkdir -p $PAPERLESS_CONSUMPTION_DIR && \
  mkdir -p $PAPERLESS_EXPORT_DIR && \
  addgroup --gid 1000 paperless && \
  adduser --home /usr/src/paperless --disabled-password --gecos "" --uid 1000 --ingroup paperless paperless

RUN echo 'Defaults env_keep += "VIRTUAL_ENV"' >>/etc/sudoers.d/paperless && \
  echo 'Defaults secure_path=/usr/src/paperless/bin:/usr/sbin:/usr/bin:/sbin:/bin' >> /etc/sudoers.d/paperless

COPY --from=builder /usr/src/paperless/ /usr/src/paperless
RUN chown -Rh paperless:paperless /usr/src/paperless

# Setup entrypoint
COPY scripts/docker-entrypoint.sh /sbin/docker-entrypoint.sh
RUN chmod 755 /sbin/docker-entrypoint.sh

# Copy gunicorn.conf
COPY scripts/gunicorn.conf.py /usr/src/paperless/

WORKDIR /usr/src/paperless/src
# Mount volumes and set Entrypoint
VOLUME ["/usr/src/paperless/data", "/usr/src/paperless/media", "/consume", "/export"]

ENTRYPOINT ["/sbin/docker-entrypoint.sh"]
CMD ["--help"]

# Copy application
COPY src/ /usr/src/paperless/src/
COPY data/ /usr/src/paperless/data/
COPY media/ /usr/src/paperless/media/

# setup venv
ENV VIRTUAL_ENV=/usr/src/paperless
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN cd /usr/src/paperless/src && \
  django-admin compilemessages

# Collect static files
RUN sudo -HEu paperless /usr/src/paperless/src/manage.py collectstatic --clear --no-input
