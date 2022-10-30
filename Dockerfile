FROM python:3.10
MAINTAINER Brian Schrader <brian@brianschrader.com>
EXPOSE 8000
WORKDIR /app


# Virtual Env
RUN pip install virtualenv
RUN (virtualenv checkup)
RUN (. checkup/bin/activate)

# Cache the requirements
COPY requirements.txt .
RUN (pip install -r requirements.txt)
RUN (pip install gunicorn)

# App setup
COPY . .

# Production Setup
CMD gunicorn liljohnnycheckup:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 4 \
    --worker-connections=100 \
    --backlog=1000 \
    -p liljohnnycheckup.pid \
    --bind=0.0.0.0:8000
