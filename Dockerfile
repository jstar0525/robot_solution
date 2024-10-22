FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y git python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

WORKDIR /home/jstar/test

RUN python3 -m pip config set global.break-system-packages true

# COPY requirements.txt ./
# RUN pip3 install -r requirements.txt