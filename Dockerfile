FROM alpine:3.10

LABEL maintainer="The Paperless Project https://github.com/the-paperless-project/paperless" \
      contributors="Guy Addadi <addadi@gmail.com>, Pit Kleyersburg <pitkley@googlemail.com>, \
        Sven Fischer <git-dev@linux4tw.de>"

# Copy Pipfiles file, init script and gunicorn.conf
COPY Pipfile* /usr/src/paperless/
COPY scripts/docker-entrypoint.sh /sbin/docker-entrypoint.sh
COPY scripts/gunicorn.conf /usr/src/paperless/

# Set export and consumption directories
ENV PAPERLESS_EXPORT_DIR=/export \
    PAPERLESS_CONSUMPTION_DIR=/consume

RUN apk add --no-cache \
      bash \
      curl \
      ghostscript \
      gnupg \
      imagemagick \
      libmagic \
      libpq \
      optipng \
      poppler \
      python3 \
      shadow \
      sudo \
      tesseract-ocr \
      tzdata \
      tesseract-ocr-data-deu \
      unpaper \
      libxslt \
      qpdf \
      libxml2 && \
    apk add --no-cache --virtual .build-dependencies \
      g++ \
      gcc \
      jpeg-dev \
      musl-dev \
      poppler-dev \
      postgresql-dev \
      python3-dev \
      zlib-dev \
      libxslt-dev \
      libxml2-dev \
      qpdf-dev

# Install python dependencies
RUN python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip pipenv setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN cd /usr/src/paperless && \
    pipenv install --skip-lock --system && \
# Remove build dependencies
    apk del .build-dependencies && \
# Create the consumption directory
    mkdir -p $PAPERLESS_CONSUMPTION_DIR && \
# Create user
    addgroup -g 1000 paperless && \
    adduser -D -u 1000 -G paperless -h /usr/src/paperless paperless && \
    chown -Rh paperless:paperless /usr/src/paperless && \
    mkdir -p $PAPERLESS_EXPORT_DIR && \
# Avoid setrlimit warnings
# See: https://gitlab.alpinelinux.org/alpine/aports/issues/11122
    echo 'Set disable_coredump false' >> /etc/sudo.conf && \
# Setup entrypoint
    chmod 755 /sbin/docker-entrypoint.sh

WORKDIR /usr/src/paperless/src
# Mount volumes and set Entrypoint
VOLUME ["/usr/src/paperless/data", "/usr/src/paperless/media", "/consume", "/export"]
ENTRYPOINT ["/sbin/docker-entrypoint.sh"]
CMD ["--help"]

# Copy application
COPY src/ /usr/src/paperless/src/
COPY data/ /usr/src/paperless/data/
COPY media/ /usr/src/paperless/media/

# Collect static files
RUN sudo -HEu paperless /usr/src/paperless/src/manage.py collectstatic --clear --no-input
