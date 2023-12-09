FROM python:3.10.5
WORKDIR /usr/src/project
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get install -y sqlite
RUN pip install --upgrade pip
COPY . .
WORKDIR /usr/src/project/app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt