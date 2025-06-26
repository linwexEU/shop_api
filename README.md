
# Shop API

## Features

1.  **Auth**
    -   Authentication & Registration
    -   **OAuth 2.0** authentication
    -   **Roles**: Customer, Owner, Admin
   
2.  **Products**
    -   Get products by **category**
    -   Get products by **search parameters**
    -   Add products via **Excel file**
    -   Get product ratings
    -   Add rating to products
    -   **Like/Dislike** ratings
    -   Reply to ratings
   
3.  **Organizations**
    -   Create organization (**Owner only**)
    -   Delete organization (**Owner only**)
    -   Get organization ratings
    -   Add rating to organizations
        
4.  **Baskets**
    -   Add products to basket (adding the same product increases its count)
    -   Remove products from basket
    -   View basket contents
    -   Send Excel file with basket contents to email
        
5.  **Orders**
    -   Create order
    -   Change order state (**Admin only**)
    -   View orders
        
6.  **Notifications**
    -   View notifications
    -   Mark notifications as read
        
7.  **Scraping**
    -   **Admin** can trigger scraping from the API
----------

## Stack

1.  FastAPI
2.  OAuth 2.0
3.  Pydantic
4.  JWT
5.  AWS SES
6.  SQLAlchemy, Alembic
7.  aiohttp, BeautifulSoup (bs4)
8.  Redis
9.  RabbitMQ
10.  Docker, Docker Compose
11.  PyTransitions (State Machine)
12.  openpyxl
13.  pytest
14.  Celery
15.  Grafana, Prometheus
----------

## Installation

### 1. Docker
```bash
docker compose build 
docker compose up
```

### 2. Manual

**Base configuration**

```bash
python -m venv venv

# Windows 
.\venv\Scripts\activate
 
# Linux/MacOS  
source venv/bin/activate

pip install -r requirements.txt
```

**Start API server**

```bash
uvicorn src.main:app --reload
```

**Start RabbitMQ consumer**

```bash
python -m src.broker.consumer
```

**Start Celery**

```bash
celery -A src.worker.app:async_celery worker --loglevel=INFO --pool=solo
```