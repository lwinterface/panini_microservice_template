FROM python:3.8.3-buster as build

RUN pip install --upgrade pip

ADD requirements/dev.txt /
ADD requirements/prod.txt /
RUN pip install -r dev.txt

FROM python:3.8.3-slim-buster

COPY --from=build /install /usr/local
COPY ./app /app
COPY ./config /config
COPY ./environments /environments
WORKDIR /app
