FROM python:3.6-slim
    WORKDIR /root/app/src
    WORKDIR /root/app
    COPY setup.* /root/app
    RUN pip install .
    COPY . /root/app
