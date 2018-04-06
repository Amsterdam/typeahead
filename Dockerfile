FROM python:3.6-slim as builder
    WORKDIR /root/app
    COPY . /root/app
    RUN pip install .
