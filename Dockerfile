FROM python:3.8.3-buster

RUN pip install --upgrade pip

ADD requirements/dev.txt /
RUN pip install -r dev.txt

WORKDIR ./

ENTRYPOINT [ "python", "-m", "app.main" ]