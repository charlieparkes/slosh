FROM python:3.8-slim

# Inspired by https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/

LABEL maintainer="Charlie Mathews <charlie@charliemathews.com>"

ARG LOG_LEVEL=INFO

ENV APP_DIR=/app \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=0 \
    LD_LIBRARY_PATH=/usr/lib

# Expose the gunicorn port.
EXPOSE 80

# Set up health check.
HEALTHCHECK CMD curl -f http://127.0.0.1/health/ || exit 1

WORKDIR ${APP_DIR}

VOLUME ["/etc/nginx/conf.d"]

ARG BUILD_DEPS=" \
    apt-utils \
"

# Add package management scripts
COPY docker/install_packages.sh /usr/bin/install_packages
COPY docker/upgrade_packages.sh /usr/bin/upgrade_packages
COPY docker/remove_packages.sh /usr/bin/remove_packages

COPY config/dpkg/01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc
COPY Pipfile Pipfile.lock ./

# Install dependencies & clean.
RUN set -ex \
    && install_packages $BUILD_DEPS \
        > /dev/null 2>&1 \
    && pip install -U pipenv \
    && pipenv install --deploy --system \
    && rm Pipfile Pipfile.lock \
    && pip uninstall -y pipenv \
    && python -m pip uninstall -y pip \
    && remove_packages $BUILD_DEPS > /dev/null 2>&1 \
    && apt-get clean \
    && rm -rf \
        $APP_DIR/.cache \
        $APP_DIR/reports \
        /usr/games \
        /usr/lib/debug \
        /usr/lib/gcc \
        /usr/local/share/.cache \
        /usr/share/doc/ \
        /usr/share/info \
        /usr/share/lintian \
        /usr/share/man/ \
        /var/lib/apt/lists/ \
        /var/log/* \
        /var/tmp/* \
        /tmp/*

# Copy service files
COPY . .
COPY docker/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Upgrade system packages to get latest security updates.
RUN set -ex \
    upgrade_packages \
    && apt-get clean \
    && rm -rf \
        /var/cache/
