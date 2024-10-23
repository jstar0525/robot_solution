FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y git python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

WORKDIR /home/jstar/test

RUN python3 -m pip config set global.break-system-packages true \
    && pip3 install pyyaml \
    && pip3 install open3d \
    && apt-get upate \
    && apt-get install -y libgl1-mesa-glx

# COPY requirements.txt ./
# RUN pip3 install -r requirements.txt