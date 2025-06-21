#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=src.worker.app:async_celery worker -l INFO
fi