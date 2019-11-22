#!/bin/bash

celery multi start worker -A home_io_backend.celery --loglevel=DEBUG

flask db upgrade
flask run --with-threads