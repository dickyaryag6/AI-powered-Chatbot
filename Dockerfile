FROM python:3.7-slim

RUN mkdir /app

WORKDIR /app

COPY . /app/

#RUN apt-get update && apt-get install -y \
#    software-properties-common
#RUN add-apt-repository universe

#RUN apt-get install \
#    python3.7 -y\
#    python3-pip -y

RUN pip3 install --upgrade pip

RUN pip3 install --default-timeout=10000 -r requirements.txt

