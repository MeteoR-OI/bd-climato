FROM python:3

ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt /home/django/app
WORKDIR /home/django/app
RUN pip3 install -r requirements.txt

