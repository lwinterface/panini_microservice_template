FROM python:3.8.3-buster

RUN pip install --upgrade pip

ADD requirements/dev.txt /
ADD requirements/prod.txt /
RUN pip install -r dev.txt

RUN mkdir /app
WORKDIR /app
COPY ./ /app