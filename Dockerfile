FROM python:3.6-slim
    WORKDIR /root/app
    COPY . /root/app/
    RUN pip install .