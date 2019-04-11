FROM amsterdam/python

ARG https_proxy=http://10.240.2.1:8080/
ENV https_proxy=$https_proxy

WORKDIR /root/app
COPY . /root/app/
RUN pip install .