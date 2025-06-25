FROM python:3.11.12-slim 

RUN apt-get update

RUN mkdir /shop_api

WORKDIR /shop_api 

COPY requirements.txt .

RUN pip install -r requirements.txt 
RUN pip install --no-deps fastapi-authlib

COPY . .

RUN chmod a+x /shop_api/docker/*.sh

CMD ["gunicorn", "src.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]