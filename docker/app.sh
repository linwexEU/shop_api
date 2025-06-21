#!/bin/bash

cd src 

alembic upgrade head 

cd .. 

gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000