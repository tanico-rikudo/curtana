FROM python:3.9.7-buster
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    tzdata \
&&  ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Tokyo

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools


RUN mkdir -p /root/src
COPY requirements.txt /root/src
WORKDIR /root/src
RUN pip install -r requirements.txt
