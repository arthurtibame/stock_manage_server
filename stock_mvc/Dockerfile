FROM ubuntu:18.04
MAINTAINER arthur8485@gmail.com

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y
RUN apt-get install mysql-server -y
RUN apt-get install libmysqlclient-dev -y

COPY requirements.txt requirements.txt
COPY Stockapp /opt/

RUN pip3 install -r requirements.txt
WORKDIR /opt/

CMD ["gunicorn3", "-b", "0.0.0.0:8000", "runserver:app", "--workers=5"]
