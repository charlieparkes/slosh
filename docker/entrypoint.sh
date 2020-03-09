#!/usr/bin/env bash

cd "$APP_DIR";

# Copy nginx config into position
cp -rf config/nginx/* /etc/nginx/conf.d


if [[ -n "$DEBUG" ]]; then
    # Reload source files while developing.
    exec gunicorn app.main:app -k uvicorn.workers.UvicornWorker --config "$APP_DIR/config/gunicorn.py" --user nobody --reload "$@";
else
    exec gunicorn app.main:app -k uvicorn.workers.UvicornWorker --config "$APP_DIR/config/gunicorn.py" --user nobody --preload "$@";
fi
