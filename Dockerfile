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

# App setup
COPY . .

# Production Setup
CMD uvicorn liljohnnycheckup:app  \
    --workers 4 \
    --no-server-header \
    --limit-max-requests 2000 \
    --backlog 1000 \
    --host 0.0.0.0 \
    --port 8000

