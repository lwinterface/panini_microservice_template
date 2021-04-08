FROM python:3.8.3-buster

RUN pip install --upgrade pip

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR ./

ENTRYPOINT [ "python", "-m", "microservice.app" ]