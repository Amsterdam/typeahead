FROM python:3.7-slim
    WORKDIR /root/app
    COPY . /root/app/
    RUN pip install .